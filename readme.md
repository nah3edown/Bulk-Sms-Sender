# Telegram SMS Bot

Telegram bot + Web Dashboard connected with SMS.NET.BD API for sending SMS messages.

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
git clone <your-repo-url>
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

Access at: `http://localhost:5000`

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

Create `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token_here
SMS_API_KEY=your_sms_api_key_here
ADMIN_IDS=123456789,987654321
PORT=5000
```

**Get these values:**
- `BOT_TOKEN`: Talk to @BotFather on Telegram
- `SMS_API_KEY`: From SMS.NET.BD dashboard
- `ADMIN_IDS`: Your Telegram user ID(s)
- `PORT`: (Optional) Default is 5000

## Deployment

### Deploy on Render

1. Push to GitHub
2. Create Render Background Worker
3. Connect your repository
4. Add Environment Variables:
   - `BOT_TOKEN`
   - `SMS_API_KEY`
   - `ADMIN_IDS`
   - `PORT` (optional, defaults to 5000)
5. Deploy

### Deploy on Other Platforms

This works on any platform supporting Python:
- Railway.app
- PythonAnywhere
- Heroku (paid)
- AWS, Google Cloud, Azure
- Your own VPS

## Project Structure

```
Bulk-Sms-Sender/
├── bot.py                 # Main Flask + Telegram app
├── templates/
│   └── index.html         # Web dashboard
├── downloads/             # Uploaded files
├── .env.example           # Environment template
├── Requirement.txt        # Python dependencies
├── Render.yaml           # Render.com config
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
- Check port 5000 is available
- Try different port: set `PORT=8000` in .env

### SMS not sending
- Verify `SMS_API_KEY` is correct
- Check SMS.NET.BD account balance
- Verify phone numbers format (88017XXXXXXXX)
- Check SMS API response in logs

### File upload fails
- File must be CSV or TXT
- Max file size: 16MB
- Check phone number format in file

## Tips

- Use `/listnumbers` to preview numbers before sending
- Test with single SMS first before bulk
- Keep admin IDs private and secure
- Monitor SMS balance regularly
- Save important SMS logs

## Support

- **SMS.NET.BD**: [sms.net.bd](https://sms.net.bd)
- **Telegram Bot API**: [core.telegram.org/bots](https://core.telegram.org/bots)
- **Flask Docs**: [flask.palletsprojects.com](https://flask.palletsprojects.com)

## License

MIT License - Free to use and modify

## Contributing

Feel free to fork, modify, and improve!

---

**Made with ❤️ for bulk SMS management**
