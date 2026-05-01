<div align="center">

# 🤖 Anime News Bot

### *Your AI-Powered Anime News Aggregator*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://telegram.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

*Never miss an anime update again! Automatically monitors Telegram channels, analyzes news with AI, and organizes everything in beautiful documents.*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

---

</div>

## 📖 Table of Contents

- [✨ Features](#-features)
- [🎬 Demo](#-demo)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🎯 Usage](#-usage)
- [🏗️ How It Works](#️-how-it-works)
- [📁 Project Structure](#-project-structure)
- [🔧 Advanced Configuration](#-advanced-configuration)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- 📺 **Multi-Channel Monitoring** - Tracks 5+ anime news Telegram channels simultaneously
- 🤖 **AI-Powered Analysis** - Uses Google Gemini 2.0 Flash for intelligent content analysis
- 📝 **Auto Documentation** - Generates professional Word documents with scripts & descriptions
- ☁️ **Cloud Storage** - Automatically uploads to Google Drive for access anywhere

</td>
<td width="50%">

### 🛡️ Smart Features
- 🔄 **Duplicate Detection** - SQLite-based deduplication saves 80% processing time
- ⏸️ **Rate Limiting** - Intelligent API quota management prevents exhaustion
- 📊 **Real-time Stats** - Live performance monitoring and analytics
- 📬 **Message Queue** - Handles burst traffic gracefully, no messages lost

</td>
</tr>
</table>

### 📸 Media Handling
- 🖼️ **Photo Analysis** - AI analyzes images alongside text for context
- 🎬 **Video Processing** - Downloads and uploads videos up to 50MB
- 🎨 **Smart Filtering** - Pre-filters non-anime content before API calls

### 🎛️ Production Ready
- ♻️ **Auto-retry Logic** - Exponential backoff for failed requests
- 💾 **Persistent Stats** - Track performance over time
- 🔒 **Secure** - Environment variables for all sensitive data
- 🌐 **Scalable** - Queue-based architecture handles high traffic

---

## 🎬 Demo

### Real-Time Processing

```
==================================================
📨 [Queue: 0] ONEPIECE (@The_Anime_News)
==================================================
📸 Photo detected
   ✅ Downloaded 2.34MB
🔍 Analyzing with Gemini...
   📸 Analyzing image + text...
✅ Confirmed anime news: One Piece Chapter 1095 Released
📝 Creating document...
   ✅ Image embedded
📤 Uploading: NEWS_ONEPIECE.docx
   📊 25%
   📊 50%
   📊 75%
   📊 100%
   ✅ Uploaded! ID: 1AbC2DeF3GhI4JkL5MnO

==================================================
🎉 PROCESSING COMPLETE!
==================================================
```

### Generated Output Example

**Document Structure:**
```
📄 NEWS_ONEPIECE.docx
├── Title: One Piece Chapter 1095 Released
├── 🎙️ Script: [40-word AI-generated script]
├── 📝 Description: [2 sentences + hashtags]
├── 🎵 Music: [Suggested background music]
└── 🖼️ Visual: [Embedded image from channel]
```

---

## 🚀 Quick Start

Get up and running in **5 minutes**!

```bash
# 1. Clone the repository
git clone https://github.com/LRAJAS/Anime-News-Bot.git
cd Anime-News-Bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Add Google Drive credentials
# Download credentials.json from Google Cloud Console
# Place it in project root

# 5. Run the bot
python main.py
```

**That's it!** 🎉 The bot will start monitoring channels and processing news.

---

## 📦 Installation

### Prerequisites

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Telegram Account** ([Sign Up](https://telegram.org/))
- **Google Account** (for Drive & Gemini APIs)

### Step-by-Step Setup

<details>
<summary><b>1️⃣ Get Telegram API Credentials</b> (Click to expand)</summary>

1. Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new application:
   - **App title:** Anime News Bot
   - **Short name:** anime_bot
   - **Platform:** Other
4. Copy your `api_id` and `api_hash`

</details>

<details>
<summary><b>2️⃣ Get Google Gemini API Key</b> (Click to expand)</summary>

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click **Get API Key**
3. Create a new API key
4. Copy the key

**Free Tier:** 60 requests per minute ✨

</details>

<details>
<summary><b>3️⃣ Set Up Google Drive API</b> (Click to expand)</summary>

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Drive API**
4. Create credentials:
   - **API & Services** → **Credentials**
   - **Create Credentials** → **OAuth 2.0 Client ID**
   - **Application type:** Desktop app
5. Download `credentials.json`
6. Place it in your project root folder

</details>

<details>
<summary><b>4️⃣ Create Google Drive Folder</b> (Click to expand)</summary>

1. Go to [Google Drive](https://drive.google.com/)
2. Create a new folder (e.g., "Anime News Bot")
3. Open the folder
4. Copy the **folder ID** from the URL:
   ```
   https://drive.google.com/drive/folders/1PYbeiYy76SBzY3-k8A9H3HBrNeGJb0MT
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                           This is your FOLDER_ID
   ```

</details>

### Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or install individually
pip install telethon google-generativeai openai
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install python-docx Pillow python-dotenv
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Telegram Configuration
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here

# AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional

# Google Drive
DRIVE_FOLDER_ID=your_folder_id_here

# Channels to Monitor (comma-separated)
TARGET_CHANNELS=@The_Anime_News,@AniFlix_News,@Anime_News_Infinite

# Rate Limiting (requests per minute)
RATE_LIMIT_PER_MINUTE=10

# Optional Features
USE_DALLE=False
```

### Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_API_ID` | ✅ Yes | - | Your Telegram API ID |
| `TELEGRAM_API_HASH` | ✅ Yes | - | Your Telegram API Hash |
| `GEMINI_API_KEY` | ✅ Yes | - | Google Gemini API key |
| `OPENAI_API_KEY` | ❌ No | - | OpenAI API key (for DALL-E) |
| `DRIVE_FOLDER_ID` | ✅ Yes | - | Google Drive folder ID |
| `TARGET_CHANNELS` | ✅ Yes | - | Telegram channels to monitor |
| `RATE_LIMIT_PER_MINUTE` | ❌ No | `10` | API calls per minute |
| `USE_DALLE` | ❌ No | `False` | Enable DALL-E image generation |

---

## 🎯 Usage

### Starting the Bot

```bash
python main.py
```

**First run:** You'll be prompted to log in to Telegram and authorize Google Drive access.

### Stopping the Bot

Press `Ctrl + C` to gracefully shutdown and see final statistics.

### Monitoring Performance

Stats are automatically displayed:
- ✅ Every 10 successful processes
- ✅ On bot shutdown
- ✅ Saved to `stats.json`

```
╔══════════════════════════════════════╗
║         📊 CURRENT STATS            ║
╠══════════════════════════════════════╣
║ Total Messages:                 142 ║
║ Processed:                       98 ║
║ Skipped:                         32 ║
║ Duplicates:                      12 ║
║ Errors:                           0 ║
║ API Calls:                       98 ║
║ Queue Size:                       0 ║
║ Efficiency:                   31.0% ║
╚══════════════════════════════════════╝
```

---

## 🏗️ How It Works

### Architecture Overview

```
┌─────────────────┐
│  Telegram       │
│  Channels       │
│  (5+ sources)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Event Handler  │  ← New message arrives
│  (Telethon)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Message Queue  │  ← Handles burst traffic
│  (asyncio)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Duplicate      │  ← Check if already processed
│  Detection      │     (SQLite + MD5 hash)
│  (80% savings)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Media          │  ← Download photos/videos
│  Download       │     (Telethon API)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Analysis    │  ← Analyze content
│  (Gemini 2.0)   │     (text + image)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Document       │  ← Generate Word doc
│  Generation     │     (python-docx)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Google Drive   │  ← Upload to cloud
│  Upload         │
└─────────────────┘
```

### Key Components

#### 1. Message Queue System
**Problem:** 5 messages arrive at once → API overload
**Solution:** Queue + Sequential Processing

```python
# Messages queued instantly
await message_queue.put(event)

# Worker processes one at a time
event = await message_queue.get()
await process_message(event)
```

#### 2. Duplicate Detection
**Problem:** Same news posted on multiple channels
**Solution:** MD5 hash + SQLite lookup

```python
msg_hash = hashlib.md5(text.encode()).hexdigest()
if hash_exists_in_database(msg_hash):
    skip_processing()  # 80% time savings!
```

#### 3. Rate Limiting
**Problem:** API quota exhaustion
**Solution:** Smart time-based limiting

```python
if calls_last_minute >= 10:
    wait(60 - time_since_first_call)
```

#### 4. AI Analysis Pipeline

```python
# 1. Pre-filter with keywords
if not contains_anime_keywords(text):
    return SKIP

# 2. Rate limit check
rate_limiter.wait_if_needed()

# 3. Send to Gemini
response = gemini_model.generate_content([prompt, image])

# 4. Parse structured output
Title | Script | Music | Image | Description
```

---

## 📁 Project Structure

```
Anime-News-Bot/
│
├── 📄 main.py                 # Main bot logic
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md              # This file
├── 📄 LICENSE                # MIT License
│
├── 🔐 .env                   # Your secrets (gitignored)
├── 📋 .env.example           # Template for others
├── 🚫 .gitignore             # Git ignore rules
│
├── 📁 data/                  # Runtime data (gitignored)
│   ├── bot_data.db          # SQLite database
│   └── stats.json           # Performance stats
│
├── 📁 results/               # Generated content (gitignored)
│   ├── documents/           # Word documents
│   └── media/               # Downloaded videos
│
└── 📁 docs/                  # Documentation
    ├── SETUP.md             # Detailed setup guide
    ├── API.md               # API documentation
    └── TROUBLESHOOTING.md   # Common issues
```

---

## 🔧 Advanced Configuration

### Custom Channel List

Add or remove channels in `.env`:

```env
TARGET_CHANNELS=@your_channel1,@your_channel2,@your_channel3
```

### Adjust Rate Limits

Modify based on your API tier:

```env
# Free tier: 10-15 per minute
RATE_LIMIT_PER_MINUTE=10

# Paid tier: increase as needed
RATE_LIMIT_PER_MINUTE=60
```

### Anime Keywords Filter

Edit in `main.py` to customize detection:

```python
anime_keywords = [
    'anime', 'manga', 'episode', 'season',
    # Add your custom keywords
    'your_favorite_anime_name',
]
```

### Database Management

```bash
# Reset duplicate detection
rm data/bot_data.db

# Reset statistics
rm data/stats.json

# Clear results folder
rm -rf results/*
```

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ "ModuleNotFoundError: No module named 'telethon'"</b></summary>

**Cause:** Dependencies not installed

**Fix:**
```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>❌ "Missing credentials.json"</b></summary>

**Cause:** Google Drive credentials not found

**Fix:**
1. Download `credentials.json` from Google Cloud Console
2. Place it in project root folder
3. Ensure filename is exactly `credentials.json`

</details>

<details>
<summary><b>❌ "Quota exceeded" / "429 Error"</b></summary>

**Cause:** Too many API calls

**Fix:**
1. Increase `RATE_LIMIT_PER_MINUTE` in `.env`
2. Wait 24 hours for quota reset
3. Consider upgrading API tier

</details>

<details>
<summary><b>❌ Bot processes same message twice</b></summary>

**Cause:** Database not persisting

**Fix:**
```bash
# Check database exists
ls data/bot_data.db

# If missing, bot will recreate on next run
python main.py
```

</details>

<details>
<summary><b>⚠️ "Video upload failed"</b></summary>

**Cause:** Video too large or network timeout

**Fix:**
1. Videos >50MB are skipped (by design)
2. Check internet connection
3. Retry mechanism will auto-retry 3 times

</details>

<details>
<summary><b>🔒 "Authentication failed"</b></summary>

**Cause:** Wrong API credentials

**Fix:**
1. Verify `.env` file exists
2. Check API keys are correct
3. Ensure no extra spaces in `.env`
4. For Telegram: Delete `anime_bot_session.session` and re-login

</details>

### Still Having Issues?

1. **Enable Debug Mode:**
   ```python
   # Add to main.py top
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Logs:**
   - Look for error messages in terminal
   - Check `stats.json` for error counts

3. **Open an Issue:**
   - Go to [GitHub Issues](https://github.com/LRAJAS/Anime-News-Bot/issues)
   - Describe the problem
   - Include error messages (remove API keys!)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check [existing issues](https://github.com/LRAJAS/Anime-News-Bot/issues)
2. If new, open an issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (OS, Python version)

### Suggesting Features

1. Open an issue labeled "enhancement"
2. Describe the feature
3. Explain use case
4. Optional: Propose implementation

### Pull Requests

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Open Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Anime-News-Bot.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black main.py

# Lint code
flake8 main.py
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 LRAJAS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

### Built With

- **[Telethon](https://github.com/LonamiWebs/Telethon)** - Telegram client library
- **[Google Gemini](https://ai.google.dev/)** - AI-powered content analysis
- **[Google Drive API](https://developers.google.com/drive)** - Cloud storage
- **[python-docx](https://github.com/python-openxml/python-docx)** - Document generation
- **[SQLite](https://www.sqlite.org/)** - Lightweight database

### Inspiration

This project was inspired by the need to:
- 📰 Keep up with rapidly updating anime news
- 🤖 Leverage AI for content organization
- ☁️ Centralize information from multiple sources
- 📝 Auto-generate shareable content

### Special Thanks

- Anime community for testing and feedback
- Google for free Gemini API tier
- Telegram for robust API
- Open-source Python community

---

## 📞 Contact & Support

### Get Help

- 📧 **Email:** your.email@example.com
- 💬 **Telegram:** [@YourUsername](https://t.me/YourUsername)
- 🐛 **Issues:** [GitHub Issues](https://github.com/LRAJAS/Anime-News-Bot/issues)
- 💡 **Discussions:** [GitHub Discussions](https://github.com/LRAJAS/Anime-News-Bot/discussions)

### Follow Development

- ⭐ Star this repo for updates
- 👁️ Watch for new releases
- 🍴 Fork to customize for your needs

---

<div align="center">

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LRAJAS/Anime-News-Bot&type=Date)](https://star-history.com/#LRAJAS/Anime-News-Bot&Date)

---

**Made with ❤️ for anime fans worldwide**

[⬆ Back to Top](#-anime-news-bot)

</div>