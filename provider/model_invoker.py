
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from openai import OpenAI
from config.config import config

class ModelInvoker:
    def __init__ (self, user_query):
        self.user_query = user_query
        self.temp = 0.0
        self.model = "gpt-4o-mini"
        self.config = config()
        self.prompt = self.build_prompt()
    
    def build_prompt(self):
        return """
        You are an expert in helping the user in his daily activities
        asnwering any question about all the topics
        Always answer in spanish and with a colombian accent
        Be friendly with the user
        Answer all the questios accuractely
        """

    def invoke_model(self, provider, history):
        try:
            if not provider:
                raise ValueError("Provider is required")
            
            if provider == "openai":
                response, total_tokens = self.invoke_open_ai(history)
            
            elif provider == "google":
                response, total_tokens = self.invoke_google(history)
            
            return response, total_tokens
        
        except Exception as e:
            logger.error(f"Error invoking model: {e}")
            return {"error": str(e)}
    

    def invoke_open_ai(self, history):
        try:
            api_key = self.config.open_ai_key
            if not api_key:
                raise ValueError("OpenAI API key is required")

            client = OpenAI(api_key=api_key)


            full_input = f"{self.prompt}\n\nHistorial:\n{history or ''}\n\nUsuario:\n{self.user_query}"

            response = client.responses.create(
                model=self.model,
                input=full_input,
                temperature=self.temp
            )

            logger.info(f"Response from OpenAI: {response}")

            output_text = response.output[0].content[0].text
            total_tokens = getattr(response.usage, "total_tokens", None)

            return output_text, total_tokens

        except Exception as e:
            logger.error(f"Error invoking OpenAI: {e}")
            raise e
        
    def invoke_google(self, history):
        return "Model is not currently available", 0