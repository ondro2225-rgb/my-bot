import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Tokenni Render muhit o'zgaruvchisidan olish
TOKEN = os.environ.get("BOT_TOKEN")

# Render port talab qilgani uchun kichik veb-server ochamiz
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Botingiz muvaffaqiyatli ishga tushdi va ishlayapti!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Siz yozdingiz: {text}")

def main():
    if not TOKEN:
        print("Xatolik: BOT_TOKEN topilmadi!")
        return

    # Veb-serverni alohida oqimda (thread) ishga tushiramiz
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()

    app = ApplicationBuilder().token(TOKEN).build()

    # /start buyrug'i uchun handler
    app.add_handler(CommandHandler("start", start))
    
    # Oddiy matnli xabarlarga javob berish uchun handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
