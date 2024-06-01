@bot.callback_query_handler(func=lambda call: call.data == "reg")
def register(call: types.CallbackQuery):
    """
    Запускает процесс регистрации нового пользователя.

    Запрашивает у пользователя логин, устанавливает состояние пользователя на "ввод логина" и отправляет сообщение
    с запросом ввода логина.
    """
    # Запрашиваем у пользователя логин
    bot.send_message(call.message.chat.id, "Введи свой логин:")
    # Установливаем состояние пользователя на "ввод логина"
    bot.set_state(call.message.chat.id, "username")


@bot.message_handler(func=lambda message: bot.get_state(message.chat.id) == "username")
def get_username(message: types.Message):
    """
    Сохраняет введенный пользователем логин и запрашивает пароль.

    Сохраняет введенный текст в качестве логина пользователя, отправляет сообщение с запросом ввода пароля и
    устанавливает состояние пользователя на "ввод пароля".
    """
    # Получаем логин пользователя и запросим пароль
    global username
    username = message.text
    bot.send_message(message.chat.id, f"Введи пароль для логина {username}:")
    # Установливаем состояние пользователя на "ввод пароля"
    bot.set_state(message.chat.id, "password")


@bot.message_handler(func=lambda message: bot.get_state(message.chat.id) == "password")
def get_password(message: types.Message):
    """
    Сохраняет введенный пользователем пароль и регистрирует его в системе.

    Сохраняет введенный текст в качестве пароля пользователя, проверяет, существует ли уже пользователь с таким
    именем пользователя, и если нет, то регистрирует нового пользователя. Если пользователь уже существует,
    отправляет сообщение об ошибке. Если регистрация прошла успешно, отправляет сообщение об успешной регистрации
    и устанавливает состояние пользователя на "None".
    """
    # Получаем пароль пользователя и зарегистрируем его
    global username
    password = message.text
    chat_id = message.chat.id
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = cursor.fetchall()
    if usernames is None:
        users = []
    else:
        # Преобразуем список кортежей в список строк
        users = [username[0] for username in usernames]
    check = check_account(chat_id)
    if check == None:
        if username in users:
            user_id = check_credentials(username, password)
            log = check_logging(chat_id, username)
            if user_id and log:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add = types.KeyboardButton("Добавить олимпиаду")
                button_mine = types.KeyboardButton("Список добавленных олимпиад")
                markup.add(button_add, button_mine)
                bot.send_message(
                    message.chat.id,
                    "Вход в систему уже осуществлен",
                    reply_markup=markup,
                )
            else:
                markup = types.InlineKeyboardMarkup()
                button_log = types.InlineKeyboardButton(
                    text="Вход в систему", callback_data="login"
                )
                button_reg = types.InlineKeyboardButton(
                    text="Регистрация в системе", callback_data="reg"
                )
                markup.add(button_log, button_reg)
                bot.send_message(
                    message.chat.id,
                    "Этот логин уже занят - попробуй снова",
                    reply_markup=markup,
                )
        else:
            register_user(message.chat.id, username, password)
            add_chatid(chat_id, username)
            # Удаляем состояние пользователя
            bot.delete_state(message.chat.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_add = types.KeyboardButton("Добавить олимпиаду")
            button_mine = types.KeyboardButton("Список добавленных олимпиад")
            markup.add(button_add, button_mine)
            add_chatid(chat_id, username)
            # Сообщаем пользователю об успешной регистрации
            bot.send_message(
                message.chat.id, "Регистрация прошла успешно!", reply_markup=markup
            )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(
            message.chat.id, f"{check}, cначала выйди из аккаунта", reply_markup=markup
        )


def register_user(user_login: int, username: str, password: str):
    """
    Регистрирует нового пользователя в базе данных.

    Устанавливает соединение с базой данных, добавляет нового пользователя и закрывает соединение.
    """
    # Добавляем нового пользователя в базу данных
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()