
import os
from dotenv import load_dotenv
load_dotenv()

class config:
    open_ai_key = os.getenv("OPEN_API_KEY", None)
    gemini_api_key = os.getenv("GEMINI_API_KEY", None)
    db_user = os.getenv("DB_USER", None)
    provider = os.getenv("PROVIDER", "google")
    db_password = os.getenv("DB_PASSWORD", None)
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    TOKEN = os.getenv("TOKEN", None)

