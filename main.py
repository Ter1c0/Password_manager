import telebot
from controllers import save_password_in_db, get_password_in_db, delete_password2, list_sites

# Load environment variables
TOKEN = "7861280594:AAEyEiBo7pxxTv4bRa4I7ebzJDDmr-Wtk-0"
bot = telebot.TeleBot(TOKEN)

# Create reply keyboard for user interaction
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🔗Сохранить пароль 🔗')
button_2 = telebot.types.KeyboardButton('📓Взять пароль📓')
button_3 = telebot.types.KeyboardButton('🗑удалить пароль🗑')
button_4 = telebot.types.KeyboardButton('📋Список сайтов📋')
keyboard.add(button_1, button_2, button_3, button_4)

# Handle the /start command to welcome users
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id, 
        'Привет, я менеджер паролей! Используйте кнопки для выполнения действий.',
        reply_markup=keyboard
    )

# Fetch and display saved passwords for the user
def get_password_from_db(message):
    passwords = get_password_in_db(message.from_user.id)
    if passwords:
        for password in passwords:
            bot.send_message(message.chat.id, f"Сайт: {password[0]}\nПароль: ||{password[1]}||\nURL: {password[2]}",parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, "У вас нет сохраненных паролей.")
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)

# Guide user through deleting a password
def delete_password_from_db(message):
    passwords = get_password_in_db(message.from_user.id)
    if passwords:
        password_list = "\n".join([f"{i+1}. {p[0]}" for i, p in enumerate(passwords)])
        bot.send_message(message.chat.id, f"Выберите номер пароля для удаления:\n{password_list}")
        bot.register_next_step_handler(message, confirm_delete, passwords)
    else:
        bot.send_message(message.chat.id, "У вас нет сохраненных паролей.")
        bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)

# Confirm deletion of the selected password
def confirm_delete(message, passwords):
    try:
        index = int(message.text) - 1
        if 0 <= index < len(passwords):
            password_to_delete = passwords[index]
            bot.send_message(message.chat.id, f"Вы уверены, что хотите удалить пароль для сайта {password_to_delete[0]}? (да/нет)")
            bot.register_next_step_handler(message, yes_no, password_to_delete)
        else:
            bot.send_message(message.chat.id, "Неверный номер. Попробуйте еще раз.")
            bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")
        bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)

# Handle user confirmation or cancellation of deletion
def yes_no(message, password_to_delete):
    if message.text.lower() == 'да'or message.text.lower() == "yes":
        # Передача расшифрованного пароля в delete_password2
        delete_password2(message.from_user.id, password_to_delete[1])
        bot.send_message(message.chat.id, f"Пароль для сайта {password_to_delete[0]} удален.")
    else:
        bot.send_message(message.chat.id, "Удаление отменено.")
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)


# Display a list of saved sites for the user
def display_sites(message):
    sites = list_sites(message.from_user.id)
    if sites:
        site_list = "\n".join([f"{i+1}. {site}" for i, site in enumerate(sites)])
        bot.send_message(message.chat.id, f"Ваши сайты:\n{site_list}")
    else:
        bot.send_message(message.chat.id, "У вас нет сохраненных сайтов.")
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)

# Main text message handler for user actions
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if '🔗Сохранить пароль 🔗' in message.text:
        bot.send_message(message.chat.id, 'Введите название сайта(пробел), пароль(пробел) и ссылку на него:\nЕсли не хотите вводить ссылку, просто введите что-то другое)')
        bot.register_next_step_handler(message, save_password_in_db, bot=bot, k=keyboard)
    elif '📓Взять пароль📓' in message.text:
        bot.send_message(message.chat.id, 'Вот ваши сохраненные пароли:')
        get_password_from_db(message)
    elif '🗑удалить пароль🗑' in message.text:
        delete_password_from_db(message)
    elif '📋Список сайтов📋' in message.text:
        display_sites(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте кнопки для выбора действия.', reply_markup=keyboard)

# Start the bot polling loop
bot.polling(non_stop=True, interval=1)
