import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Tokenlarni tekshirish
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    print("Xatolik: BOT_TOKEN topilmadi!")
    exit(1)

if not GEMINI_API_KEY:
    print("Xatolik: GEMINI_API_KEY topilmadi!")
    exit(1)

# Gemini API ni to'g'ri sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Flask server (Render talabini bajarish uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "HELLO, WORLD!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Telegram xabarlariga javob berish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {str(e)}")

def main():
    # Flask serverni alohida ishga tushiramiz
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Telegram botni ishga tushiramiz
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
