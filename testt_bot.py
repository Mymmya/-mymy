import subprocess
import sys

# Автоустановка
try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters
except ImportError:
    print("Устанавливаю python-telegram-bot...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot"])
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters

import asyncio
from telegram.ext import ContextTypes

TOKEN = 8684934800:AAHgLrRN59SWfOrtU-0p8MQEmZ0vUwsMEOQ"

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
