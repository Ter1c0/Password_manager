from models import TodoList
from datetime import datetime, timedelta
import database
import telebot

# Dictionary to store user sessions
sessions = {}

# Define session duration (2 hours)
SESSION_DURATION = timedelta(hours=2)

# Register a new user
def register_user(user_id):
    db = database.Database()
    db.execute(
        "INSERT OR IGNORE INTO users (userId, registered_at) VALUES (?, ?)",
        (user_id, datetime.now().isoformat())
    )
    db.commit()

# Log in an existing user
def login_user(user_id):
    db = database.Database()
    cursor = db.execute("SELECT registered_at FROM users WHERE userId = ?", (user_id,))
    if cursor.fetchone():
        sessions[user_id] = datetime.now()
        return True
    return False

# Check if the session is still active
def is_session_active(user_id):
    if user_id in sessions:
        last_login = sessions[user_id]
        if datetime.now() - last_login < SESSION_DURATION:
            return True
    return False

# Save a password in the database
def save_password_in_db(m, bot, k):
    if not is_session_active(m.from_user.id):
        bot.send_message(m.chat.id, 'Ваша сессия истекла. Войдите снова с помощью /login.')
        return
    sait, pas, url = m.text.split()
    user_id = m.from_user.id
    todo = TodoList(user_id)
    todo.add_sait(sait, pas, url)
    bot.send_message(message.chat.id, 'Хорошо, я сохранил!')
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=k)

# Retrieve passwords from the database
def get_password_in_db(user_id):
    if not is_session_active(user_id):
        return None
    todo = TodoList(user_id)
    return todo.get_sait()

# Delete a specific password from the database
def delete_password2(user_id, password):
    if not is_session_active(user_id):
        return
    todo = TodoList(user_id)
    todo.delete_password(password)
