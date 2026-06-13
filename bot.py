import os
import logging
import requests
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SMS_API_KEY = os.getenv("SMS_API_KEY")

ADMIN_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip()
]

SMS_URL = "https://api.sms.net.bd/sendsms"
DOWNLOADS_DIR = "downloads"

# Create downloads directory if it doesn't exist
Path(DOWNLOADS_DIR).mkdir(exist_ok=True)


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Access denied.")
        return

    await update.message.reply_text(
        "✅ SMS Bot Online\n\n"
        "/send <number> <message>\n"
        "/bulk <number1,number2> <message>\n"
        "/upload - Upload CSV/TXT file with numbers\n"
        "/balance"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    try:
        url = "https://api.sms.net.bd/user/balance/"
        response = requests.get(
            url,
            params={"api_key": SMS_API_KEY},
            timeout=30
        )

        await update.message.reply_text(
            f"Balance Response:\n{response.text}"
        )

    except Exception as e:
        await update.message.reply_text(str(e))


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/send 88017XXXXXXXX Hello"
        )
        return

    number = context.args[0]
    message = " ".join(context.args[1:])

    try:
        payload = {
            "api_key": SMS_API_KEY,
            "to": number,
            "msg": message
        }

        response = requests.post(
            SMS_URL,
            data=payload,
            timeout=30
        )

        await update.message.reply_text(
            f"SMS Response:\n{response.text}"
        )

    except Exception as e:
        await update.message.reply_text(str(e))


async def bulk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "/bulk 88017XXXX,88018XXXX Hello Everyone"
        )
        return

    numbers = context.args[0]
    message = " ".join(context.args[1:])

    try:
        payload = {
            "api_key": SMS_API_KEY,
            "to": numbers,
            "msg": message
        }

        response = requests.post(
            SMS_URL,
            data=payload,
            timeout=60
        )

        await update.message.reply_text(
            f"Bulk SMS Response:\n{response.text}"
        )

    except Exception as e:
        await update.message.reply_text(str(e))


async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /upload command - ask user to send file"""
    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "📁 Please send a CSV or TXT file with phone numbers\n\n"
        "File format:\n"
        "• CSV: One phone number per line or comma-separated\n"
        "• TXT: One phone number per line\n\n"
        "Example:\n"
        "88017XXXXXXXX\n"
        "88018XXXXXXXX\n"
        "88019XXXXXXXX"
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads"""
    if not is_admin(update.effective_user.id):
        return

    document = update.message.document

    # Check file type
    if not document.file_name.endswith(('.csv', '.txt')):
        await update.message.reply_text("❌ Please send a CSV or TXT file")
        return

    try:
        # Download file
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(DOWNLOADS_DIR, document.file_name)
        await file.download_to_drive(file_path)

        # Read and parse phone numbers
        phone_numbers = parse_phone_numbers(file_path)

        if not phone_numbers:
            await update.message.reply_text("❌ No valid phone numbers found in file")
            return

        # Store for later use
        context.user_data['phone_numbers'] = phone_numbers
        context.user_data['file_name'] = document.file_name

        await update.message.reply_text(
            f"✅ File uploaded successfully!\n\n"
            f"Found {len(phone_numbers)} phone numbers\n\n"
            f"Now send the message you want to send to these numbers:\n"
            f"Example: /sendfile Your message here"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error processing file: {str(e)}")


def parse_phone_numbers(file_path: str) -> list:
    """Parse phone numbers from CSV or TXT file"""
    phone_numbers = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by newlines and commas
        lines = content.replace(',', '\n').split('\n')

        for line in lines:
            phone = line.strip()
            if phone and phone.isdigit():
                phone_numbers.append(phone)

        return phone_numbers

    except Exception as e:
        logging.error(f"Error parsing file: {str(e)}")
        return []


async def sendfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send SMS to all numbers from uploaded file"""
    if not is_admin(update.effective_user.id):
        return

    if 'phone_numbers' not in context.user_data:
        await update.message.reply_text(
            "❌ No file uploaded yet. Use /upload to upload a file first"
        )
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage:\n/sendfile Your message here")
        return

    phone_numbers = context.user_data['phone_numbers']
    message = " ".join(context.args)
    numbers_str = ",".join(phone_numbers)

    try:
        payload = {
            "api_key": SMS_API_KEY,
            "to": numbers_str,
            "msg": message
        }

        response = requests.post(
            SMS_URL,
            data=payload,
            timeout=120
        )

        await update.message.reply_text(
            f"✅ SMS sent to {len(phone_numbers)} numbers\n\n"
            f"Response: {response.text}"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error sending SMS: {str(e)}")


async def list_numbers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List currently loaded phone numbers"""
    if not is_admin(update.effective_user.id):
        return

    if 'phone_numbers' not in context.user_data:
        await update.message.reply_text("❌ No file uploaded yet")
        return

    phone_numbers = context.user_data['phone_numbers']
    file_name = context.user_data.get('file_name', 'Unknown')

    # Create message with first 10 numbers (avoid too long message)
    numbers_preview = "\n".join(phone_numbers[:10])
    remaining = len(phone_numbers) - 10

    message = (
        f"📄 File: {file_name}\n"
        f"Total numbers: {len(phone_numbers)}\n\n"
        f"Preview:\n{numbers_preview}"
    )

    if remaining > 0:
        message += f"\n... and {remaining} more"

    await update.message.reply_text(message)


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN missing")

    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send))
    app.add_handler(CommandHandler("bulk", bulk))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("upload", upload_command))
    app.add_handler(CommandHandler("sendfile", sendfile_command))
    app.add_handler(CommandHandler("listnumbers", list_numbers_command))

    # File handler for document uploads
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
