import os
import sys
import logging
import httpx

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.schemas import RequestModel, AnswerModel, ErrorModel
from services.process import ProcessRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
TELEGRAM_TOKEN = os.getenv("TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not OPENAI_API_KEY:
    logger.error("Variable de entorno OPEN_API_KEY no definida")
    raise RuntimeError("OPEN_API_KEY is required")
if not TELEGRAM_TOKEN:
    logger.error("Variable de entorno TOKEN no definida")
    raise RuntimeError("TOKEN is required")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = FastAPI(
    title="Telegram Bot via Webhook",
    description="Recibe mensajes de Telegram y responde"
)

@app.get("/health", summary="Health Check")
async def health():
    return {"status": "OK", "message": "Server is running"}

@app.post("/webhook", summary="Telegram updates endpoint")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        logger.info(f"Update recibido: {update}")

        message = update.get("message")
        if not message:
            return JSONResponse(status_code=400, content={"error": "No message field in update"})

        chat_id = message["chat"]["id"]
        user_input = message.get("text", "")

        if not user_input:
            await send_reply(chat_id, "Lo siento, sólo puedo procesar texto por ahora.")
            return {"ok": True}


        procesador = ProcessRequest(user_query=user_input, chat_id=chat_id)
        response_text = procesador.process_request()


        await send_reply(chat_id, response_text)

        return {"ok": True}

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})

    except Exception as exc:
        logger.error(f"Error en webhook: {exc}")
        return JSONResponse(status_code=500, content={"error": str(exc)})

async def send_reply(chat_id: int, text: str):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        if resp.status_code != 200:
            logger.error(f"Error enviando mensaje a Telegram: {resp.text}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
