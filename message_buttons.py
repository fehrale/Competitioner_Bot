@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: telebot.types.CallbackQuery) -> None:
    """Обрабатывает нажатия на кнопки в сообщениях с инлайн-клавиатурой.

    Функция проверяет, есть ли у пользователя учетная запись. Если учетная запись есть, 
    обрабатывает нажатия на кнопки в зависимости от их обратного вызова. Если учетной 
    записи нет, отправляет пользователю сообщение с просьбой войти в систему.
    """
    global selected_olympiad, delete_ol
    chat_id = call.message.chat.id
    check = check_account(chat_id)
    if check:
        element = call.data
        if "save" in element:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_delete = types.KeyboardButton("Удалить")
            button_no = types.KeyboardButton("Оставить все как есть")
            markup.add(button_delete, button_no)
            element = element[4:]
            delete_ol = element
            bot.send_message(
                call.message.chat.id,
                f"Описание олимпиады: {olympics[element]}",
                reply_markup=markup,
            )
        else:
            selected_olympiad = element
            bot.send_message(
                call.message.chat.id,
                f"Описание олимпиады: {olympics[element]}",
            )
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_yes = types.KeyboardButton("Да")
            button_no = types.KeyboardButton("Нет")
            markup.add(button_yes, button_no)
            bot.send_message(
                call.message.chat.id,
                "Добавить олимпиаду в список выбранных?",
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
            call.message.chat.id,
            "Для начала нужно зарегистрироваться или войти в аккаунт:",
            reply_markup=markup,
        )