# Telegram SMS Bot

Telegram bot connected with SMS.NET.BD API for sending bulk SMS messages.

## Features

- 📱 Send single SMS messages
- 📢 Send bulk SMS to multiple recipients
- 📁 Upload CSV/TXT files with phone numbers
- 💰 Check account balance
- 🔐 Admin-only access control

## Commands

### Send Single SMS

```text
/send 88017XXXXXXXX Hello
```

### Send Bulk SMS (Direct)

```text
/bulk 88017XXXXXXXX,88018XXXXXXXX Offer Available
```

### Upload Phone Numbers from File

```text
/upload
```

Then send a CSV or TXT file containing phone numbers.

**File Format:**
- CSV: One phone number per line or comma-separated
- TXT: One phone number per line

**Example file content:**
```
88017XXXXXXXX
88018XXXXXXXX
88019XXXXXXXX
```

### Send SMS to Uploaded Numbers

After uploading a file with `/upload`, use:

```text
/sendfile Your message here
```

This will send the message to all phone numbers from the uploaded file.

### List Loaded Phone Numbers

```text
/listnumbers
```

Shows a preview of the currently loaded phone numbers from the uploaded file.

### Check Balance

```text
/balance
```

## Environment Variables

Create a `.env` file with the following variables:

```env
BOT_TOKEN=your_telegram_bot_token
SMS_API_KEY=your_sms_api_key
ADMIN_IDS=user_id_1,user_id_2,user_id_3
```

## Deploy on Render

1. Push project to GitHub
2. Create Render Background Worker
3. Connect repository
4. Add environment variables in Render dashboard:
   - `BOT_TOKEN`
   - `SMS_API_KEY`
   - `ADMIN_IDS`
5. Deploy

## Requirements

- Python 3.8+
- See `Requirement.txt` for dependencies

## Installation

```bash
pip install -r Requirement.txt
```

## Running Locally

```bash
# Create .env file
cp .env.example .env

# Install dependencies
pip install -r Requirement.txt

# Run bot
python bot.py
```

## Usage Workflow

### Single SMS
1. Start bot with `/start`
2. Use `/send <number> <message>`

### Bulk SMS (Direct)
1. Start bot with `/start`
2. Use `/bulk <number1,number2,number3> <message>`

### Bulk SMS (From File)
1. Use `/upload` to start file upload
2. Send a CSV or TXT file with phone numbers
3. Use `/listnumbers` to preview the numbers
4. Use `/sendfile <message>` to send SMS to all numbers
5. Repeat for new file or numbers

## Security

- ✅ Admin-only access - Only specified admin IDs can use the bot
- ✅ Secure token handling via environment variables
- ✅ Input validation for phone numbers
- ✅ Timeout protection for API requests

## Support

For issues with SMS API, visit [SMS.NET.BD](https://sms.net.bd)

For Telegram Bot API documentation, visit [Telegram Bot API](https://core.telegram.org/bots/api)
