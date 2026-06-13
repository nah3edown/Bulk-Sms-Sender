import os
import logging
import requests

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
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


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN missing")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send))
    app.add_handler(CommandHandler("bulk", bulk))
    app.add_handler(CommandHandler("balance", balance))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
