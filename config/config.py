
import os
from dotenv import load_dotenv
load_dotenv()

class config:
    open_ai_key = os.getenv("OPEN_API_KEY", None)
    gemini_api_key = os.getenv("GEMINI_API_KEY", None)
    db_user = os.getenv("DB_USER", None)
    db_password = os.getenv("DB_PASSWORD", None)

