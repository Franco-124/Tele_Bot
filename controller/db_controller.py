
from db.sql import db

class DbController:

    def __init__ (self):
        self.db = db()

    def save_message(self, chat_id, role, content, total_tokens):
        self.db.save_message(chat_id, role, content, total_tokens)

    def get_history(self, chat_id):
        return self.db.get_history(chat_id)