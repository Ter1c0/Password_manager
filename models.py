from database import Database
from cryptography.fernet import Fernet
import os
class Todo:
    def __init__(self, id, user_id, website, url, password):
        self.id = id
        self.user_id = user_id
        self.website = website
        self.url = url
        self.password = password

class TodoList:
    def __init__(self, user_id):
        self.tasks = []
        self.user_id = user_id
        self.db = Database()
        self.cipher = Fernet(os.getenv("ENCRYPTION_KEY"))

    def add_sait(self, sait, pas, url):
        encrypted_password = self.cipher.encrypt(pas.encode()).decode()
        self.db.execute(
            "INSERT INTO tasks (userId, website, password, url1) VALUES (?, ?, ?, ?)",
            (self.user_id, sait, encrypted_password, url)
        )
        self.db.commit()

    def get_sait(self):
        cursor = self.db.execute(
            "SELECT website, password, url1 FROM tasks WHERE userId = ?",
            (self.user_id,)
        )
        return [(row[0], self.cipher.decrypt(row[1].encode()).decode(), row[2]) for row in cursor.fetchall()]

    def delete_password(self, password):
        encrypted_password = self.cipher.encrypt(password.encode()).decode()
        self.db.execute(
            "DELETE FROM tasks WHERE userId = ? AND password = ?",
            (self.user_id, encrypted_password)
        )
        self.db.commit()