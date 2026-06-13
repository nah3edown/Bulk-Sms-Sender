# Telegram SMS Bot

Telegram bot + Web Dashboard connected with SMS.NET.BD API for sending SMS messages.

## 🚀 Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/nah3edown/Bulk-Sms-Sender)

## Features

- 📱 Send single SMS messages via Telegram or Web
- 📢 Send bulk SMS to multiple recipients
- 📁 Upload CSV/TXT files with phone numbers
- 💰 Check account balance
- 🔐 Admin-only access control
- 🌐 Beautiful web dashboard interface
- 🤖 Full Telegram bot integration

## Quick Start

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from @BotFather)
- SMS.NET.BD API Key
- Admin Telegram User IDs

### Installation

```bash
# Clone repository
git clone https://github.com/nah3edown/Bulk-Sms-Sender.git
cd Bulk-Sms-Sender

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r Requirement.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### Running Locally

```bash
python bot.py
```

The bot will:
- Start polling Telegram for messages
- Start Flask web server on http://localhost:5000

Access the web dashboard at: **http://localhost:5000**

## Usage

### Via Telegram Bot

#### Commands

- `/start` - Show available commands
- `/send <number> <message>` - Send single SMS
- `/bulk <numbers> <message>` - Send to multiple numbers
- `/upload` - Upload CSV/TXT file
- `/sendfile <message>` - Send to uploaded numbers
- `/listnumbers` - Show preview of uploaded numbers
- `/balance` - Check account balance

#### Examples

```
/send 88017XXXXXXXX Hello World

/bulk 88017XXXXXXXX,88018XXXXXXXX Check this out!

/upload
[Send file]

/sendfile Great offer available!

/balance
```

### Via Web Dashboard

Access at: `http://localhost:5000` or `https://your-render-app.onrender.com`

**Features:**
- 📤 **Single SMS Tab** - Send to one number
- 📢 **Bulk SMS Tab** - Send to multiple numbers at once
- 📁 **Upload File Tab** - Upload CSV/TXT and send bulk SMS
- 💰 **Balance Tab** - Check SMS balance

## File Format (CSV/TXT)

### TXT Format
```
88017XXXXXXXX
88018XXXXXXXX
88019XXXXXXXX
```

### CSV Format
```
88017XXXXXXXX,88018XXXXXXXX,88019XXXXXXXX
```

Or with one number per line:
```
88017XXXXXXXX
88018XXXXXXXX
88019XXXXXXXX
```

## Environment Variables

Create `.env` file or set in your hosting platform:

```env
BOT_TOKEN=your_telegram_bot_token_here
SMS_API_KEY=your_sms_api_key_here
ADMIN_IDS=123456789,987654321
PORT=5000
```

**Get these values:**
- `BOT_TOKEN`: Talk to @BotFather on Telegram
- `SMS_API_KEY`: From SMS.NET.BD dashboard
- `ADMIN_IDS`: Your Telegram user ID(s) (comma-separated)
- `PORT`: (Optional) Default is 5000

## Deployment

### Option 1: Deploy on Render (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/nah3edown/Bulk-Sms-Sender)

Or manually:

1. Go to [Render.com](https://render.com)
2. Click "New +" → "Background Worker"
3. Connect your GitHub repository
4. Set environment variables:
   - `BOT_TOKEN`
   - `SMS_API_KEY`
   - `ADMIN_IDS`
5. Deploy!

### Option 2: Deploy on Other Platforms

Works on any platform supporting Python:
- **Railway.app** - Simple, free tier available
- **PythonAnywhere** - Beginner-friendly
- **AWS, Google Cloud, Azure** - Enterprise options
- **Your own VPS** - Full control

### Option 3: Run Locally 24/7

Keep your computer on and run:
```bash
python bot.py
```

## Project Structure

```
Bulk-Sms-Sender/
├── bot.py                 # Main Flask + Telegram app
├── templates/
│   └── index.html         # Web dashboard
├── downloads/             # Uploaded files (auto-created)
├── .env.example           # Environment template
├── .env                   # Your credentials (not tracked)
├── Requirement.txt        # Python dependencies
├── Render.yaml           # Render.com configuration
├── .gitignore            # Git ignore rules
└── readme.md             # This file
```

## API Endpoints (Web)

- `POST /api/send-single` - Send single SMS
- `POST /api/send-bulk` - Send bulk SMS
- `POST /api/upload` - Upload file
- `POST /api/send-file` - Send to uploaded numbers
- `GET /api/get-balance` - Get account balance
- `GET /api/get-uploaded` - Get uploaded file info

## Security

✅ **Admin-only access** - Only specified admin IDs can use bot/dashboard
✅ **Secure credentials** - All secrets in environment variables
✅ **Input validation** - Phone numbers validated before sending
✅ **File size limits** - Max 16MB file uploads
✅ **Rate limiting** - Built-in request timeouts
✅ **HTTPS ready** - Works with SSL/TLS

## Troubleshooting

### Bot not responding
- Check `BOT_TOKEN` is correct
- Verify bot is running: `python bot.py`
- Check logs for errors

### Web dashboard not loading
- Verify Flask is installed: `pip install Flask`
- Check port 5000 is available or set different PORT
- Try different port: set `PORT=8000` in .env

### SMS not sending
- Verify `SMS_API_KEY` is correct
- Check SMS.NET.BD account balance
- Verify phone numbers format (88017XXXXXXXX for Bangladesh)
- Check SMS API response in logs

### File upload fails
- File must be CSV or TXT
- Max file size: 16MB
- Check phone number format in file
- One number per line or comma-separated

## Tips

- Use `/listnumbers` to preview numbers before sending
- Test with single SMS first before bulk
- Keep admin IDs and credentials private and secure
- Monitor SMS balance regularly with `/balance`
- Save important SMS logs for your records
- Test locally before deploying to production

## Support

- **SMS.NET.BD**: [sms.net.bd](https://sms.net.bd)
- **Telegram Bot API**: [core.telegram.org/bots](https://core.telegram.org/bots)
- **Flask Docs**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Render Docs**: [render.com/docs](https://render.com/docs)

## License

MIT License - Free to use and modify

## Contributing

Feel free to fork, modify, and improve!

## How to Get Your Credentials

### 1. Telegram Bot Token
- Open Telegram and search for @BotFather
- Send `/start` then `/newbot`
- Follow the instructions
- Copy your BOT_TOKEN

### 2. SMS.NET.BD API Key
- Visit [SMS.NET.BD](https://sms.net.bd)
- Create account and verify
- Go to API settings
- Copy your API_KEY

### 3. Your Admin ID
- Send a message to your bot
- Check bot logs to see your user ID
- Or use `/start` and check the logs

## Changelog

- **v1.0** - Initial release with Telegram bot + Web dashboard
- Added file upload functionality
- Added web dashboard with Flask
- Multi-admin support

---

**Made with ❤️ for bulk SMS management**

Questions? Issues? Feel free to open an issue on GitHub!
