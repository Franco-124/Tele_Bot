
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from openai import OpenAI
import google.generativeai as genai
from config.config import config

class ModelInvoker:
    def __init__ (self, user_query, user_name):
        self.user_query = user_query
        self.user_name = user_name
        self.temp = 0.0
        self.model = "gpt-4o-mini"
        self.config = config()
        self.prompt = self.build_prompt(user_name)
    

    def user_settings(self):
        try:
            return {
                "emoji": True,
                "language": "spanish",
                "tone": "formal",
            }
        
        except Exception as e:
            logger.error(f"Error retrieving user settings: {e}")
            raise e

    def build_prompt(self, user_name: str):
        settings = self.user_settings()
        emoji = settings.get("emoji", True)
        language = settings.get("language", "spanish")
        tone = settings.get("tone", "formal")
        return (
            f"You are PrimeAI, a formal and professional financial assistant dedicated to supporting {user_name}. "
            "Provide clear, precise, and financially sound guidance based on best practices and established principles. "
            "If there is no previous conversation history, start with this first message: "
            f"{'Use emojis in your responses ' if emoji else 'Do not use emojis in your responses '}"
            f"ALWAYS Respond in {language} with a {tone} tone. "
            "\"Hello, I hope you're doing well. My name is PrimeAI, your financial assistant. I'm here to help you understand, plan, and make informed financial decisions. How may I assist you today?\" "
            "If there is conversation history, continue naturally without repeating the first message."
        )
            
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
        try:
            if not self.config.gemini_api_key:
                raise ValueError("Gemini API key is required")
                
            genai.configure(api_key=self.config.gemini_api_key)

            model = genai.GenerativeModel('gemini-2.5-flash')

            full_input = f"{self.prompt}\n\nHistorial:\n{history or ''}\n\nUsuario:\n{self.user_query}"

            response = model.generate_content(
                full_input,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temp
                )
            )
            output_text = response.text
            
            total_tokens = 0
            if response.usage_metadata:
                total_tokens = response.usage_metadata.total_token_count

            logger.info(f"Response from Google Gemini: {output_text[:50]}...") 

            return output_text, total_tokens
        
        except Exception as e:
            logger.error(f"Error invoking Google Gemini: {e}")
            raise e