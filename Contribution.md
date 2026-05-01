# Contributing to Anime News Bot

First off, thank you for considering contributing! 🎉

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, etc.)

**Template:**
```
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 10]
 - Python Version: [e.g. 3.11]
 - Bot Version: [e.g. 1.0.0]
```

### Suggesting Features

Feature requests are welcome! Please:

1. **Check existing feature requests**
2. **Provide clear use case**
3. **Explain expected behavior**
4. **Optional: Suggest implementation**

### Pull Requests

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**PR Guidelines:**
- ✅ Clear description of changes
- ✅ Test your code
- ✅ Follow existing code style
- ✅ Update documentation if needed
- ✅ Add comments for complex logic

## 💻 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Anime-News-Bot.git
cd Anime-News-Bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your test credentials
```

## 📝 Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions small and focused

**Example:**
```python
def process_message(event):
    """
    Process a single message from the queue.
    
    Args:
        event: Telethon event object containing message data
        
    Returns:
        None
        
    Raises:
        Exception: If processing fails after retries
    """
    # Your code here
```

## 🧪 Testing

Before submitting PR:

```bash
# Test locally
python main.py

# Check for errors
# Ensure no sensitive data in code
# Test with different message types
```

## 🎯 Priority Areas

Looking for contribution ideas? These areas need help:

1. **Testing** - Unit tests, integration tests
2. **Documentation** - Tutorials, examples, translations
3. **Features** - See "good first issue" label
4. **Bug Fixes** - Check open issues

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy towards others

## 🙏 Recognition

Contributors will be:
- Listed in README
- Mentioned in release notes
- Given credit in commits

## ❓ Questions?

Feel free to:
- Open an issue with "question" label
- Start a discussion
- Contact maintainers directly

Thank you for contributing! 🚀