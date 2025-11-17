import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
from supabase import Client, create_client
from config.config import config

class db:

    def __init__ (self):
        self.supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

    def save_message (self, 
        chat_id: str, 
        role: str, 
        content: str, 
        total_tokens: int):

        try:

            data = {
                "chat_id": chat_id,
                "role": role,
                "content": content,
                "total_tokens": total_tokens
            }

            logger.info(f"Guardando mensaje: {data}")
            self.supabase.table("agent_history").insert(data).execute()

            logger.info("Mensaje guardado exitosamente")    
        
        except Exception as e:
            logger.error(f"Error al guardar el mensaje: {e}")
            raise e

    def get_history(self, chat_id: str):
        try:

            logger.info("Recuperando historial")

            history = self.supabase.table("agent_history")\
            .select("*")\
            .eq("chat_id", chat_id)\
            .execute()
            logger.info("Historial recuperado exitosamente")
            return history.data

        except Exception as e:
            logger.error(f"Error al recuperar el historial: {e}")
            raise e
        


  