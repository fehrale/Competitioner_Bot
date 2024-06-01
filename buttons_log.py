@bot.callback_query_handler(func=lambda call: call.data == "login")
def login(call: types.CallbackQuery):
    """
    Запускает процесс входа в систему для пользователя.

    Запрашивает у пользователя логин, устанавливает состояние пользователя на "ввод логина" и отправляет сообщение
    с запросом ввода логина.
    """
    # Запрашиваем у пользователя логин
    bot.send_message(call.message.chat.id, "Введи свой логин:")
    # Устанавливаем состояние пользователя на "ввод логина"
    bot.set_state(call.message.chat.id, "username_log")


# Обработаем ввод логина
@bot.message_handler(
    func=lambda message: bot.get_state(message.chat.id) == "username_log"
)
def get_username(message: types.Message):
    """
    Сохраняет введенный пользователем логин и запрашивает пароль.

    Сохраняет введенный текст в качестве логина пользователя, отправляет сообщение с запросом ввода пароля и
    устанавливает состояние пользователя на "ввод пароля".
    """
    # Получаем логин пользователя и запрашиваем пароль
    global username
    username = message.text
    bot.send_message(message.chat.id, f"Введи пароль для логина {username}:")
    # Установливаем состояние пользователя на "ввод пароля"
    bot.set_state(message.chat.id, "password_log")


# Обработаем ввод пароля
@bot.message_handler(
    func=lambda message: bot.get_state(message.chat.id) == "password_log"
)
def get_password(message: types.Message):
    """
    Сохраняет введенный пользователем пароль и проверяет его.

    Сохраняет введенный текст в качестве пароля пользователя, проверяет его и в зависимости от результата проверки
    отправляет сообщение об успешной авторизации или об ошибке. Удаляет состояние пользователя.
    """
    # Получаем пароль пользователя и проверяем его
    global username
    chat_id = message.chat.id
    password = message.text
    user_id = check_credentials(username, password)
    check = check_account(chat_id)
    if check == None:
        # Если пользователь авторизован
        if user_id:
            if check_logging(chat_id, username):
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
                # Сообщаем пользователю об успешной авторизации
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add = types.KeyboardButton("Добавить олимпиаду")
                button_mine = types.KeyboardButton("Список добавленных олимпиад")
                markup.add(button_add, button_mine)
                add_chatid(chat_id, username)
                bot.send_message(
                    message.chat.id,
                    "Авторизация прошла успешно! Можешь добавить олимпиаду или посмотреть уже сохраненные",
                    reply_markup=markup,
                )
        # Если пользователь не авторизован
        else:
            markup = types.InlineKeyboardMarkup()
            button_log = types.InlineKeyboardButton(
                text="Вход в систему", callback_data="login"
            )
            button_reg = types.InlineKeyboardButton(
                text="Регистрация в системе", callback_data="reg"
            )
            markup.add(button_log, button_reg)
            # Сообщаем пользователю о том, что данные введены неверно
            bot.send_message(
                message.chat.id,
                "Неверные данные для входа. Попробуй еще раз",
                reply_markup=markup,
            )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(
            message.chat.id, f"{check}, cначала выйди из аккаунта", reply_markup=markup
        )
    # Удаляем состояние пользователя
    bot.delete_state(message.chat.id)