import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from provider.model_invoker import ModelInvoker
from controller.db_controller import DbController

class ProcessRequest:
    def __init__(self, message: str, chat_id: str):
        self.message = message
        self.chat_id = chat_id
        self.model_invoker = ModelInvoker(message=self.message)
        self.db_controller = DbController()

    def process_request(self):
        try:
            history = self.get_history_from_db()
            logger.info(f"Invoking model with message {self.message} and history {history}")
            response = self.model_invoker.invoke_model(provider="openai", history=history)
            if "error" in response:
                return "Hubo un error tratanto de dar respuesta a la solicitud, Por favor intente de nuevo mas tarde"
            
            return response
        
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return "Error procesando la solicitud, Por favor intente de nuevo mas tarde"
    
    def get_history_from_db(self):
        try:

            history = self.db_controller.get_history(chat_id=self.chat_id)
            return history

        except Exception as e:
            logger.error(f"Error getting history from db: {e}")
            raise e
