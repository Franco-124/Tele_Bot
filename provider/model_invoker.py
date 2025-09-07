
from openai import OpenAI
from config.config import config

class ModelInvoker:
    def __init__ (self, message):
        self.message = message
        self.temp = 0.0
        self.model = "gpt-4.1-mini"
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
                response = self.invoke_open_ai(history)
            
            elif provider == "google":
                response = self.invoke_google(history)
            
            return response
        
        except Exception as e:
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
                {"role": "system", "content": self.message},
                {"role": "user", "content": self.prompt},
            ],
            )
            return response.choices[0].message.content
        
        except TimeoutError as e:
            raise TimeoutError(f"Timeout error {e}")
        
        except ValueError as e:
            raise ValueError(f"Value error {e}")
        
        except Exception as e:
            raise e
        
    def invoke_google(self, history):
        return "Model is not currently available"