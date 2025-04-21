
#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
changed 5
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from config import *



import json
import os
import difflib
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# 🔐 Конфигурация

#env variables
import os
TOKEN = os.getenv('TOKEN')
SOURCE_CHAT_ID = os.getenv('SOURCE_CHAT_ID ')
TARGET_CHAT_ID = os.getenv('TARGET_CHAT_ID')

STORAGE_FILE = "messages_log.json"
SIMILARITY_THRESHOLD = 0.9  # насколько похожие смс считаются "одинаковыми"

# 📁 Загрузка и сохранение
def load_messages():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_messages(messages):
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# 🤖 Проверка похожести сообщений
def is_similar(text, existing_messages):
    return False
    for msg in existing_messages:
        similarity = difflib.SequenceMatcher(None, text, msg["text"]).ratio()
        if similarity >= SIMILARITY_THRESHOLD:
            print(msg["text"], similarity)
            return True
    return False

# 🔄 Основной обработчик
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    msg_text = update.message.text
    msg_id = update.message.message_id
    chat_id = update.message.chat_id

    # Обрабатываем только сообщения из нужного канала
    if chat_id != SOURCE_CHAT_ID:
        return

    messages = load_messages()

    if is_similar(msg_text, messages):
        print("Сообщение слишком похоже на уже отправленные. Пропускаем.")
        return

    # Отправка сообщения в целевую группу
    await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=msg_text)
    print(f"✅ Отправлено сообщение: {msg_text[:50]}...")

    # Сохраняем в историю
    messages.append({
        "message_id": msg_id,
        "text": msg_text
    })
    save_messages(messages)

# ▶️ Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Бот запущен и слушает GRAFAFA_NX_PROD...")
    app.run_polling()

if __name__ == "__main__":
    main()
