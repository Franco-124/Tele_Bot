import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from provider.model_invoker import ModelInvoker
class ProcessRequest:
    def __init__(self, message: str):
        self.message = message
        self.model_invoker = ModelInvoker(message=self.message)

    def process_request(self):
        try:
            history = self.get_history_from_db()
            logger.info(f"Invoking model with message {self.message}")
            response = self.model_invoker.invoke_model(provider="openai", history=history)
            if "error" in response:
                return "Hubo un error tratanto de dar respuesta a la solicitud, Por favor intente de nuevo mas tarde"
            
            return response
        
        except Exception as e:
            return "Error procesando la solicitud, Por favor intente de nuevo mas tarde"
    
    def get_history_from_db(self):
        return "Metodo para obtener el historial de la base de datos"
