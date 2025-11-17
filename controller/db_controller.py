
from db.sql import db

class DbController:

    @staticmethod
    def save_message(chat_id, role, content, total_tokens):
        db.save_message(chat_id, role, content, total_tokens)

    @staticmethod
    def get_history(chat_id):
        return db.get_history(chat_id)