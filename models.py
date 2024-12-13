from database import Database
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Class representing a single to-do (password entry)
class Todo:
    def __init__(self, id, user_id, website, url, password):
        self.id = id
        self.user_id = user_id
        self.website = website
        self.url = url
        self.password = password

# Class for managing a user's password list
class TodoList:
    def __init__(self, user_id):
        self.tasks = []
        self.user_id = user_id
        self.db = Database()
        
        # Load the encryption key from .env
        load_dotenv()
        encryption_key = os.getenv("ENCRYPTION_KEY")

        # Check if the key is missing and raise an error
        if not encryption_key:
            raise RuntimeError("Ошибка: ENCRYPTION_KEY отсутствует в .env. Создайте ключ вручную.")

        # Initialize the cipher with the existing key
        self.cipher = Fernet(encryption_key)

    # Add a new password to the database
    def add_sait(self, sait, pas, url):
        encrypted_password = self.cipher.encrypt(pas.encode()).decode()
        self.db.execute(
            "INSERT INTO tasks (userId, website, password, url1) VALUES (?, ?, ?, ?)",
            (self.user_id, sait, encrypted_password, url)
        )
        self.db.commit()

    # Retrieve all passwords for the user
    def get_sait(self):
        cursor = self.db.execute(
            "SELECT website, password, url1 FROM tasks WHERE userId = ?",
            (self.user_id,)
        )
        return [(row[0], self.cipher.decrypt(row[1].encode()).decode(), row[2]) for row in cursor.fetchall()]

    # Delete a specific password from the database
    def delete_password(self, password):
        # Найти зашифрованный пароль, соответствующий расшифрованному
        cursor = self.db.execute(
            "SELECT password FROM tasks WHERE userId = ?",
            (self.user_id,)
        )
        for row in cursor.fetchall():
            decrypted_password = self.cipher.decrypt(row[0].encode()).decode()
            if decrypted_password == password:
                encrypted_password = row[0]
                break
        else:
            return  # Если пароль не найден, ничего не делать

        # Удалить запись из базы данных
        self.db.execute(
            "DELETE FROM tasks WHERE userId = ? AND password = ?",
            (self.user_id, encrypted_password)
        )
        self.db.commit()
