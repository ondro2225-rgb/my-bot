import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Sun'iy intellekt uslubidagi javob strukturasi
    reply_text = f"Sun'iy intellekt javobi: Siz yozdingiz: {user_text}"
    await update.message.reply_text(reply_text)
if __name__ == '__main__':
    import os
TOKEN = os.environ.get("BOT_TOKEN")"8904241919:AAF4zd42fM_TmkM5gac6T7D_Dkkegshwzkg"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()
