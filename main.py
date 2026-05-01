import asyncio
import os
import io
import pickle
import time
import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
from telethon import TelegramClient, events, types
import google.generativeai as genai
from openai import OpenAI
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from docx import Document
from docx.shared import Inches
from dotenv import load_dotenv

# ==========================================
#  LOAD ENVIRONMENT VARIABLES
# ==========================================
load_dotenv()

# ==========================================
#  USER CONFIGURATION (from .env file)
# ==========================================

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DRIVE_FOLDER_ID = os.getenv('DRIVE_FOLDER_ID')

# Parse channels from comma-separated string
channels_str = os.getenv('TARGET_CHANNELS', '')
TARGET_CHANNELS = [ch.strip() for ch in channels_str.split(',') if ch.strip()]

RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '10'))
USE_DALLE = os.getenv('USE_DALLE', 'False').lower() == 'true'

CLIENT_SECRET_FILE = 'credentials.json'

# ==========================================
#  SYSTEM SETUP
# ==========================================

client = TelegramClient('anime_bot_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

openai_client = OpenAI(api_key=OPENAI_API_KEY) if USE_DALLE else None

# ⭐ MESSAGE QUEUE - Handles simultaneous messages
message_queue = asyncio.Queue()
processing_active = False

# ==========================================
#  DATABASE - DUPLICATE DETECTION
# ==========================================

def init_database():
    """Initialize SQLite database for duplicate tracking"""
    db = sqlite3.connect('bot_data.db')
    db.execute('''CREATE TABLE IF NOT EXISTS processed 
                  (msg_hash TEXT PRIMARY KEY, 
                   timestamp INTEGER, 
                   channel TEXT,
                   title TEXT)''')
    db.commit()
    return db

db = init_database()

def is_duplicate(text, channel):
    """Check if message was already processed"""
    msg_hash = hashlib.md5(text.encode()).hexdigest()
    
    cursor = db.execute('SELECT title FROM processed WHERE msg_hash = ?', (msg_hash,))
    result = cursor.fetchone()
    
    if result:
        print(f"   ♻️ Duplicate: {result[0]}")
        return True
    
    return False

def mark_as_processed(text, channel, title):
    """Mark message as processed"""
    msg_hash = hashlib.md5(text.encode()).hexdigest()
    try:
        db.execute('INSERT INTO processed VALUES (?, ?, ?, ?)', 
                   (msg_hash, int(time.time()), channel, title))
        db.commit()
    except sqlite3.IntegrityError:
        pass

# ==========================================
#  STATS TRACKING
# ==========================================

stats = {
    'total_messages': 0,
    'processed': 0,
    'skipped': 0,
    'duplicates': 0,
    'errors': 0,
    'api_calls': 0,
    'queue_size': 0,
    'start_time': time.time()
}

def load_stats():
    """Load stats from file"""
    try:
        with open('stats.json', 'r') as f:
            loaded = json.load(f)
            loaded['start_time'] = time.time()
            return loaded
    except:
        return stats.copy()

def save_stats():
    """Save stats to file"""
    stats['uptime_hours'] = (time.time() - stats['start_time']) / 3600
    stats['queue_size'] = message_queue.qsize()
    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

def print_stats():
    """Print current stats"""
    efficiency = 0
    if stats['total_messages'] > 0:
        efficiency = 100 - (stats['api_calls'] / stats['total_messages'] * 100)
    
    print(f"""
╔══════════════════════════════════════╗
║         📊 CURRENT STATS            ║
╠══════════════════════════════════════╣
║ Total Messages: {stats['total_messages']:>18} ║
║ Processed:      {stats['processed']:>18} ║
║ Skipped:        {stats['skipped']:>18} ║
║ Duplicates:     {stats['duplicates']:>18} ║
║ Errors:         {stats['errors']:>18} ║
║ API Calls:      {stats['api_calls']:>18} ║
║ Queue Size:     {stats['queue_size']:>18} ║
║ Efficiency:     {efficiency:>17.1f}% ║
╚══════════════════════════════════════╝
    """)

stats = load_stats()

# ==========================================
#  RATE LIMITING
# ==========================================

class RateLimiter:
    """Smart rate limiter to prevent quota exhaustion"""
    def __init__(self, calls_per_minute=10):
        self.calls = []
        self.limit = calls_per_minute
    
    def wait_if_needed(self):
        """Wait if rate limit reached"""
        now = datetime.now()
        
        # Remove calls older than 1 minute
        self.calls = [t for t in self.calls if now - t < timedelta(minutes=1)]
        
        if len(self.calls) >= self.limit:
            oldest_call = self.calls[0]
            wait_time = 60 - (now - oldest_call).seconds
            if wait_time > 0:
                print(f"⏸️ Rate limit reached. Waiting {wait_time}s...")
                time.sleep(wait_time)
                self.calls = []
        
        self.calls.append(now)

rate_limiter = RateLimiter(calls_per_minute=RATE_LIMIT_PER_MINUTE)

# ==========================================
#  GOOGLE DRIVE AUTHENTICATION
# ==========================================

def authenticate_drive():
    """Authenticates using personal Google Account"""
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                print(f"❌ ERROR: Missing {CLIENT_SECRET_FILE}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

drive_service = authenticate_drive()

# ==========================================
#  CORE FUNCTIONS
# ==========================================

def analyze_with_gemini(text, image_bytes=None, has_video=False):
    """Analyze text + image with Gemini (rate-limited)"""
    
    # Pre-filter keywords to save API calls
    anime_keywords = [
        'anime', 'manga', 'episode', 'season', 'crunchyroll', 'one piece', 
        'naruto', 'bleach', 'demon slayer', 'attack on titan', 'jujutsu',
        'spy family', 'dragon ball', 'death note', 'hunter', 'evangelion',
        'oshi no ko', 'kaguya', 'schedule', 'date', 'author', 'final'
    ]
    
    if not any(keyword in text.lower() for keyword in anime_keywords):
        print("⏭️ No anime keywords found")
        return None
    
    # Rate limit check
    rate_limiter.wait_if_needed()
    
    # Build prompt
    if has_video:
        media_note = "Note: This has a video (not analyzed to save tokens)."
    elif image_bytes:
        media_note = "Note: Analyze the image with the text."
    else:
        media_note = "Note: No media."
    
    prompt = f"""{media_note}

Text: "{text}"

If anime news, return pipe-separated:
Title (6 words)|Script (40 words)|Music|Image status|Description (2 sentences + hashtags)

If NOT anime, return: SKIP"""
    
    # Retry logic with exponential backoff
    for attempt in range(3):
        try:
            stats['api_calls'] += 1
            
            if image_bytes and not has_video:
                print("   📸 Analyzing image + text...")
                import PIL.Image
                img = PIL.Image.open(io.BytesIO(image_bytes))
                response = gemini_model.generate_content([prompt, img])
            else:
                if has_video:
                    print("   📝 Analyzing text only (video uploaded separately)")
                else:
                    print("   📝 Analyzing text only")
                response = gemini_model.generate_content(prompt)
            
            result = response.text.strip()
            
            if "SKIP" in result or "|" not in result:
                return None
            
            parts = result.split('|')
            return parts if len(parts) >= 5 else None
            
        except Exception as e:
            error_str = str(e)
            
            # Handle quota errors with retry
            if "429" in error_str or "quota" in error_str.lower():
                print(f"⚠️ Quota hit. Retry {attempt + 1}/3")
                if attempt < 2:
                    wait = 15 * (attempt + 1)
                    print(f"   Waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print("❌ Quota exhausted")
                    return None
            else:
                print(f"❌ Analysis error: {e}")
                return None
    
    return None

def upload_to_drive(local_path):
    """Upload file to Google Drive with retry logic"""
    if not drive_service:
        print("❌ Drive service not available")
        return False
    
    print(f"📤 Uploading: {os.path.basename(local_path)}")
    
    for attempt in range(3):
        try:
            file_metadata = {
                'name': os.path.basename(local_path), 
                'parents': [DRIVE_FOLDER_ID]
            }
            
            # Use resumable upload with chunking
            media = MediaFileUpload(
                local_path, 
                resumable=True, 
                chunksize=1024*1024
            )
            
            request = drive_service.files().create(
                body=file_metadata, 
                media_body=media, 
                fields='id'
            )
            
            # Execute with progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    if progress % 25 == 0:
                        print(f"   📊 {progress}%", end='\r')
            
            print(f"\n   ✅ Uploaded! ID: {response.get('id')}")
            return True
            
        except Exception as e:
            error_str = str(e).lower()
            if attempt < 2 and ("timeout" in error_str or "timed out" in error_str):
                wait = 5 * (attempt + 1)
                print(f"\n   ⚠️ Timeout. Retry {attempt + 1}/3 in {wait}s...")
                time.sleep(wait)
            else:
                print(f"\n   ❌ Upload failed: {e}")
                return False
    
    return False

def create_doc(name, parts, image_bytes=None):
    """Create Word document and upload to Drive"""
    print("📝 Creating document...")
    
    doc = Document()
    doc.add_heading(parts[0].strip(), 0)
    
    doc.add_heading('🎙️ Script:', level=1)
    doc.add_paragraph(parts[1].strip())
    
    doc.add_heading('📝 Description:', level=1)
    doc.add_paragraph(parts[4].strip())
    
    doc.add_heading('🎵 Music:', level=1)
    doc.add_paragraph(parts[2].strip())
    
    if image_bytes:
        try:
            doc.add_heading('🖼️ Visual:', level=1)
            stream = io.BytesIO(image_bytes)
            doc.add_picture(stream, width=Inches(4))
            print("   ✅ Image embedded")
        except Exception as e:
            print(f"   ⚠️ Image embed failed: {e}")
    
    filename = f"{name}.docx"
    doc.save(filename)
    success = upload_to_drive(filename)
    
    # Cleanup
    try:
        os.remove(filename)
    except:
        pass
    
    return success

# ==========================================
#  ⭐ MESSAGE PROCESSOR (runs in queue)
# ==========================================

async def process_message(event):
    """Process a single message from the queue"""
    try:
        stats['total_messages'] += 1
        
        if not event.text:
            return

        # Create safe filename
        safe_name = "".join([c for c in event.text[:15] if c.isalnum()]) or "news"
        channel = event.chat.username or "unknown"
        
        print(f"\n{'='*50}")
        print(f"📨 [Queue: {message_queue.qsize()}] {safe_name} (@{channel})")
        print(f"{'='*50}")

        # Check for duplicates
        if is_duplicate(event.text, channel):
            stats['duplicates'] += 1
            stats['skipped'] += 1
            save_stats()
            return

        image_bytes = None
        video_path = None
        has_video = False

        # Download media if present
        if event.message.media:
            if isinstance(event.message.media, types.MessageMediaPhoto):
                print("📸 Photo detected")
                try:
                    buffer = io.BytesIO()
                    await client.download_media(event.message, file=buffer)
                    buffer.seek(0)
                    image_bytes = buffer.read()
                    size_mb = len(image_bytes) / (1024 * 1024)
                    print(f"   ✅ Downloaded {size_mb:.2f}MB")
                    
                    # Skip if too large
                    if size_mb > 10:
                        print("   ⚠️ Too large, skipping")
                        image_bytes = None
                except Exception as e:
                    print(f"   ❌ Photo download failed: {e}")
            
            elif isinstance(event.message.media, types.MessageMediaDocument):
                print("🎬 Video/Document detected")
                has_video = True
                try:
                    print("   ⬇️ Downloading...")
                    video_path = await client.download_media(
                        event.message, 
                        file=f"temp_{safe_name}"
                    )
                    if video_path:
                        size = os.path.getsize(video_path) / (1024 * 1024)
                        print(f"   ✅ Downloaded {size:.1f}MB")
                    else:
                        print("   ⚠️ Download returned None")
                        has_video = False
                except Exception as e:
                    print(f"   ❌ Video download failed: {e}")
                    has_video = False

        # Analyze with Gemini
        print("🔍 Analyzing with Gemini...")
        parts = analyze_with_gemini(
            text=event.text, 
            image_bytes=image_bytes, 
            has_video=has_video
        )
        
        # If analysis failed, upload video anyway (if exists)
        if not parts:
            stats['skipped'] += 1
            save_stats()
            
            if video_path and os.path.exists(video_path):
                print("⚠️ Analysis failed, but uploading video...")
                success = upload_to_drive(video_path)
                try:
                    os.remove(video_path)
                    if success:
                        print("   ✅ Video uploaded (no script generated)")
                except:
                    pass
            return
        
        print(f"✅ Confirmed anime news: {parts[0]}")

        # Mark as processed
        mark_as_processed(event.text, channel, parts[0])

        # Create and upload document
        create_doc(f"NEWS_{safe_name}", parts, image_bytes)

        # Upload video separately if exists
        if video_path and os.path.exists(video_path):
            print("🎬 Uploading video to Drive...")
            upload_to_drive(video_path)
            try:
                os.remove(video_path)
            except:
                pass

        stats['processed'] += 1
        save_stats()

        print(f"\n{'='*50}")
        print("🎉 PROCESSING COMPLETE!")
        print(f"{'='*50}\n")
        
        # Print stats every 10 successful processes
        if stats['processed'] % 10 == 0:
            print_stats()

    except Exception as e:
        stats['errors'] += 1
        save_stats()
        print(f"\n💥 PROCESSING ERROR: {e}")
        
        # Cleanup video file on error
        if 'video_path' in locals() and video_path:
            try:
                os.remove(video_path)
            except:
                pass

# ==========================================
#  ⭐ QUEUE WORKER
# ==========================================

async def queue_worker():
    """Background worker that processes queued messages one by one"""
    global processing_active
    processing_active = True
    
    print("🔄 Queue worker started - processing messages sequentially")
    
    while processing_active:
        try:
            # Wait for message from queue
            event = await message_queue.get()
            
            # Process it
            await process_message(event)
            
            # Mark as done
            message_queue.task_done()
            
        except Exception as e:
            print(f"💥 Queue worker error: {e}")
            await asyncio.sleep(1)
    
    print("🛑 Queue worker stopped")

# ==========================================
#  EVENT HANDLER (just queues messages)
# ==========================================

@client.on(events.NewMessage(chats=TARGET_CHANNELS))
async def handler(event):
    """
    NEW MESSAGE HANDLER
    Just adds to queue - processing happens in queue_worker
    """
    await message_queue.put(event)
    
    # Notify if queue is building up
    queue_size = message_queue.qsize()
    if queue_size > 1:
        print(f"📥 Message queued (total in queue: {queue_size})")

# ==========================================
#  STARTUP
# ==========================================

print("\n" + "="*60)
print("🤖 ANIME NEWS BOT - QUEUE VERSION")
print("="*60)
print(f"📺 Monitoring Channels:")
for channel in TARGET_CHANNELS:
    print(f"   • {channel}")
print("\n✨ Features:")
print("   ✅ Message Queue → Handles burst messages")
print("   ✅ Sequential Processing → One at a time")
print("   ✅ Duplicate Detection → Saves processing")
print("   ✅ Stats Tracking → Monitor performance")
print("   ✅ Rate Limiting → Prevents quota issues")
print("   ✅ Smart Analysis → Photos + text analyzed")
print("\n📦 How it works:")
print("   1. New messages → Added to queue")
print("   2. Queue worker → Processes one by one")
print("   3. Rate limiter → Prevents API overload")
print("   4. No historical scanning (only new messages)")
print("\n🎯 Press Ctrl+C to see stats and exit")
print("="*60 + "\n")

print_stats()

try:
    print("🔌 Starting Telegram client...")
    client.start()
    print("✅ Connected!\n")
    
    # Start queue worker in background
    loop = client.loop
    loop.create_task(queue_worker())
    print("🔄 Queue worker running\n")
    
    print("🎯 Monitoring messages...\n")
    
    # Run forever
    client.run_until_disconnected()
    
except KeyboardInterrupt:
    print("\n\n⚠️ Shutting down gracefully...")
    processing_active = False
    save_stats()
    db.close()
    print_stats()
    print("\n✅ Goodbye!\n")
except Exception as e:
    print(f"\n💥 STARTUP ERROR: {e}")
    save_stats()
    db.close()
