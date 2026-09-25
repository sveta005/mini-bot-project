# Personal Music Server

A lightweight music server that supports searching, automatic metadata tagging (iTunes ID3 tags and cover art), and streaming tracks via a mobile-friendly web interface.

---

## Getting Started

### 1. Install Dependencies
```bash
pip install flask yt-dlp mutagen requests
```
### 2. Run the application
```bash
    python web_app.py
```
### 3. Run the Telegram Bot (Optional)

1. Add your Telegram Bot API token in the script (or environment variable):
   ```python
   BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

### Run bot script
```bash
    python bot.py
```
