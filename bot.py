import os
import logging
import requests
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import threading
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Load environment variables
load_dotenv()

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

# Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = DOWNLOADS_DIR

# Store uploaded numbers globally
uploaded_numbers = {}


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ============= TELEGRAM BOT FUNCTIONS =============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Access denied.")
        return

    await update.message.reply_text(
        "✅ SMS Bot Online\n\n"
        "📱 /send <number> <message>\n"
        "📢 /bulk <number1,number2> <message>\n"
        "📁 /upload - Upload CSV/TXT file\n"
        "📤 /sendfile <message>\n"
        "📋 /listnumbers\n"
        "💰 /balance\n\n"
        "Or use the web dashboard!"
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
            f"✅ SMS sent!\nResponse: {response.text}"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


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
            f"✅ Bulk SMS sent!\nResponse: {response.text}"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "📁 Please send a CSV or TXT file with phone numbers\n\n"
        "File format:\n"
        "• CSV: One per line or comma-separated\n"
        "• TXT: One per line\n\n"
        "Example:\n"
        "88017XXXXXXXX\n"
        "88018XXXXXXXX\n"
        "88019XXXXXXXX"
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    document = update.message.document

    if not document.file_name.endswith(('.csv', '.txt')):
        await update.message.reply_text("❌ Please send a CSV or TXT file")
        return

    try:
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(DOWNLOADS_DIR, document.file_name)
        await file.download_to_drive(file_path)

        phone_numbers = parse_phone_numbers(file_path)

        if not phone_numbers:
            await update.message.reply_text("❌ No valid phone numbers found in file")
            return

        context.user_data['phone_numbers'] = phone_numbers
        context.user_data['file_name'] = document.file_name

        await update.message.reply_text(
            f"✅ File uploaded!\n"
            f"Found {len(phone_numbers)} phone numbers\n\n"
            f"Send message: /sendfile Your message"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def parse_phone_numbers(file_path: str) -> list:
    phone_numbers = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

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
    if not is_admin(update.effective_user.id):
        return

    if 'phone_numbers' not in context.user_data:
        await update.message.reply_text("❌ No file uploaded. Use /upload first")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /sendfile Your message here")
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
            f"✅ SMS sent to {len(phone_numbers)} numbers!\n"
            f"Response: {response.text}"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def list_numbers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if 'phone_numbers' not in context.user_data:
        await update.message.reply_text("❌ No file uploaded yet")
        return

    phone_numbers = context.user_data['phone_numbers']
    file_name = context.user_data.get('file_name', 'Unknown')

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


# ============= FLASK WEB ROUTES =============

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/send-single', methods=['POST'])
def send_single():
    try:
        data = request.json
        number = data.get('number', '').strip()
        message = data.get('message', '').strip()

        if not number or not message:
            return jsonify({'success': False, 'error': 'Number and message required'}), 400

        payload = {
            "api_key": SMS_API_KEY,
            "to": number,
            "msg": message
        }

        response = requests.post(SMS_URL, data=payload, timeout=30)

        return jsonify({
            'success': True,
            'message': 'SMS sent successfully',
            'response': response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/send-bulk', methods=['POST'])
def send_bulk():
    try:
        data = request.json
        numbers = data.get('numbers', '').strip()
        message = data.get('message', '').strip()

        if not numbers or not message:
            return jsonify({'success': False, 'error': 'Numbers and message required'}), 400

        payload = {
            "api_key": SMS_API_KEY,
            "to": numbers,
            "msg": message
        }

        response = requests.post(SMS_URL, data=payload, timeout=60)

        return jsonify({
            'success': True,
            'message': 'Bulk SMS sent successfully',
            'response': response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not file.filename.endswith(('.csv', '.txt')):
            return jsonify({'success': False, 'error': 'Only CSV and TXT files allowed'}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        phone_numbers = parse_phone_numbers(file_path)

        if not phone_numbers:
            return jsonify({'success': False, 'error': 'No valid phone numbers found'}), 400

        uploaded_numbers['data'] = phone_numbers
        uploaded_numbers['filename'] = file.filename
        uploaded_numbers['count'] = len(phone_numbers)

        return jsonify({
            'success': True,
            'message': f'File uploaded successfully',
            'count': len(phone_numbers),
            'filename': file.filename
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/send-file', methods=['POST'])
def send_file():
    try:
        if 'data' not in uploaded_numbers:
            return jsonify({'success': False, 'error': 'No file uploaded. Please upload first'}), 400

        data = request.json
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400

        numbers_str = ",".join(uploaded_numbers['data'])

        payload = {
            "api_key": SMS_API_KEY,
            "to": numbers_str,
            "msg": message
        }

        response = requests.post(SMS_URL, data=payload, timeout=120)

        return jsonify({
            'success': True,
            'message': f'SMS sent to {len(uploaded_numbers["data"])} numbers',
            'response': response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/get-balance', methods=['GET'])
def get_balance():
    try:
        url = "https://api.sms.net.bd/user/balance/"
        response = requests.get(url, params={"api_key": SMS_API_KEY}, timeout=30)

        return jsonify({
            'success': True,
            'balance': response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/get-uploaded', methods=['GET'])
def get_uploaded():
    if 'data' in uploaded_numbers:
        preview = uploaded_numbers['data'][:10]
        remaining = len(uploaded_numbers['data']) - 10

        return jsonify({
            'success': True,
            'filename': uploaded_numbers['filename'],
            'count': uploaded_numbers['count'],
            'preview': preview,
            'remaining': max(0, remaining)
        })
    else:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400


def run_bot():
    """Run Telegram bot in separate thread"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN missing")

    app_bot = Application.builder().token(BOT_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("send", send))
    app_bot.add_handler(CommandHandler("bulk", bulk))
    app_bot.add_handler(CommandHandler("balance", balance))
    app_bot.add_handler(CommandHandler("upload", upload_command))
    app_bot.add_handler(CommandHandler("sendfile", sendfile_command))
    app_bot.add_handler(CommandHandler("listnumbers", list_numbers_command))
    app_bot.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("🤖 Telegram Bot started...")
    app_bot.run_polling()


if __name__ == "__main__":
    # Run bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Run Flask app
    port = int(os.getenv("PORT", 5000))
    print(f"🌐 Web Dashboard: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
