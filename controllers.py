from models import TodoList

# Save a password in the database
def save_password_in_db(m, bot, k):
    sait, pas, url = m.text.split()
    user_id = m.from_user.id
    todo = TodoList(user_id)
    todo.add_sait(sait, pas, url)
    bot.send_message(m.chat.id, 'Хорошо, я сохранил!')
    bot.send_message(m.chat.id, 'Что вы хотите сделать?', reply_markup=k)

# Retrieve passwords from the database
def get_password_in_db(user_id):
    todo = TodoList(user_id)
    return todo.get_sait()

# Delete a specific password from the database
def delete_password2(user_id, password):
    todo = TodoList(user_id)
    todo.delete_password(password)


# Retrieve a list of all saved sites
def list_sites(user_id):
    todo = TodoList(user_id)
    return [entry[0] for entry in todo.get_sait()]
