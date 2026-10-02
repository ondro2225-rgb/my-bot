import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Tokenlar
TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") # Render'ga bu kalitni ham qo'shish kerak

# Gemini mijozini ishga tushirish
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Render port talabini qondirish uchun Flask server
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot AI bilan ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men Gemini AI bilan ishlaydigan aqlli botman. Menga xohlagan savolingizni bering!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Foydalanuvchiga bot o'ylab turganini bildirish uchun
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Gemini AI'dan javob olish
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        reply_text = "Kechirasiz, javob olishda xatolik yuz berdi."
        print(f"Xato: {e}")

    await update.message.reply_text(reply_text)

def main():
    if not TELEGRAM_TOKEN:
        print("Xatolik: BOT_TOKEN topilmadi!")
        return

    # Veb-serverni alohida oqimda ishga tushiramiz
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Aqlli bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
