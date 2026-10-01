import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Tokenni Render muhit o'zgaruvchisidan olish
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Botingiz muvaffaqiyatli ishga tushdi va ishlayapti!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Siz yozdingiz: {text}")

def main():
    if not TOKEN:
        print("Xatolik: BOT_TOKEN topilmadi!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # /start buyrug'i uchun handler
    app.add_handler(CommandHandler("start", start))
    
    # Oddiy matnli xabarlarga javob berish uchun handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
