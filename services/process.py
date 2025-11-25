import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from provider.model_invoker import ModelInvoker
from controller.db_controller import DbController

class ProcessRequest:
    def __init__(self, user_query: str, chat_id: str, user_name: str):
        self.user_query = user_query
        self.chat_id = chat_id
        self.user_name = user_name
        self.model_invoker = ModelInvoker(user_query=self.user_query, user_name=self.user_name)
        self.db_controller = DbController()

    def process_request(self):
        try:
            history = self.get_history_from_db()
            logger.info(f"Invoking model with message {self.user_query} and history {history} and user name {self.user_name}")
            response, total_tokens = self.model_invoker.invoke_model(provider="openai", history=history , user_name=self.user_name)
            if "error" in response:
                return "Hubo un error tratando de dar respuesta a la solicitud, Por favor intente de nuevo mas tarde"
            
            self.save_message(role="user", content=self.user_query, total_tokens=total_tokens)
            self.save_message(role="assistant", content=response, total_tokens=total_tokens)
            return response
        
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return "Error procesando la solicitud, Por favor intente de nuevo mas tarde"
    
    def get_history_from_db(self):
        try:
            logger.info(f"Getting history from db for chat_id: {self.chat_id}")

            history = self.db_controller.get_history(chat_id=self.chat_id)
            history_messages = []
            for message in history:
                history_messages.append({"role": message.get("role"), "content": message.get("content")})
            return history_messages

        except Exception as e:
            logger.error(f"Error getting history from db: {e}")
            raise e
    
    def save_message(self, role: str, content: str, total_tokens: int):
        try:
            logger.info(f"Saving message to db: {content}")
            self.db_controller.save_message(
                chat_id=self.chat_id,
                role=role,
                content=content,
                total_tokens=total_tokens
            )
        
        except Exception as e:
            logger.error(f"Error saving message to db: {e}")
            raise e
