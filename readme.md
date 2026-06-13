# Telegram SMS Bot

Telegram bot connected with SMS.NET.BD API for sending bulk SMS messages.

## Features

- 📱 Send single SMS messages
- 📢 Send bulk SMS to multiple recipients
- 💰 Check account balance
- 🔐 Admin-only access control

## Commands

### Send Single SMS

```text
/send 88017XXXXXXXX Hello
```

### Send Bulk SMS

```text
/bulk 88017XXXXXXXX,88018XXXXXXXX Offer Available
```

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
