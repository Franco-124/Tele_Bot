
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from openai import OpenAI
from config.config import config

class ModelInvoker:
    def __init__ (self, user_query):
        self.user_query = user_query
        self.temp = 0.0
        self.model = "gpt-5-nano"
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

            response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "assistant", "content": history},
                {"role": "user", "content": self.user_query},
            ],
            )
            logger.info(f"Response from OpenAI: {response}")
            return response.choices[0].message.content , response.usage.total_tokens
        
        except TimeoutError as e:
            logger.error(f"Timeout error {e}")
            raise TimeoutError(f"Timeout error {e}")
        
        except ValueError as e:
            logger.error(f"Value error {e}")
            raise ValueError(f"Value error {e}")
        
        except Exception as e:
            logger.error(f"Error invoking OpenAI: {e}")
            raise e
        
    def invoke_google(self, history):
        return "Model is not currently available", 0