# Telegram SMS Bot

Telegram bot connected with SMS.NET.BD API.

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

## Deploy on Render

1. Push project to GitHub
2. Create Render Background Worker
3. Connect repository
4. Add environment variables:

BOT_TOKEN
SMS_API_KEY
ADMIN_IDS

5. Deploy
