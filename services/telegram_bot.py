import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.process import ProcessRequest
from config.config import config
import logging
import uuid

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = config.TOKEN
logger.info(f"Token: {TOKEN}")

def generate_session_id():
    return str(uuid.uuid4())

async def start(update, context):
    session_id = generate_session_id()
    context.user_data["session_id"] = session_id
    await update.message.reply_text("¡Hola! Soy tu asistente 🤖. Escríbeme algo.")

async def handle_message(update, context):
    user_input = update.message.text
    chat_id = update.effective_chat.id  

    procces = ProcessRequest(user_query=user_input, chat_id=chat_id)
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
