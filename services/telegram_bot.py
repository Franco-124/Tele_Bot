import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.process import ProcessRequest
from config.config import config
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = config.TOKEN
logger.info(f"Token: {TOKEN}")

async def start(update, context):
    await update.message.reply_text("¡Hola! Soy tu asistente 🤖. Escríbeme algo.")

async def handle_message(update, context):
    user_input = update.message.text
    procces = ProcessRequest(user_input)
    response = procces.process_request()
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()