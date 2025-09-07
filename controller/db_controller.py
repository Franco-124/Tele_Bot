
from db.sql import db

TABLA = "TeleBot"
class DbController:

    def insert(self,data):
        return db.insert(TABLA, data)

    def remove(self,data):
        return db.remove(data)

    def update(self, data):
        return db.update(TABLA, data)
    
    def get_one(self,data, id):
        return db.get(data, id)
    
    def get_all(self, data):
        return db.get_all(TABLA, data)