@bot.message_handler(content_types="text")
def message_reply(message: telebot.types.Message) -> None:
    """
    Обрабатывает введенные пользователем сообщения.

    Функция проверяет, есть ли у пользователя учетная запись. Если учетная запись есть, обрабатывает 
    сообщения в зависимости от их содержания. Если учетной записи нет, отправляет пользователю 
    сообщение с просьбой войти в систему или зарегистрироваться.
    """
    global selected_olympiad, delete_ol
    chat_id = message.chat.id
    check = check_account(chat_id)
    if check:
        if message.text == "Добавить олимпиаду":
            markup = types.InlineKeyboardMarkup()
            for ol in olympics:
                markup.add(types.InlineKeyboardButton(text=f"{ol}", callback_data=ol))
            bot.send_message(
                message.chat.id, "Список всех олимпиад:", reply_markup=markup
            )
        elif message.text == "Список добавленных олимпиад":
            save_olympiks = save_olympiads(check)
            if save_olympiks:
                markup = types.InlineKeyboardMarkup()
                for ol in save_olympiks:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f"{ol}", callback_data="save" + ol
                        )
                    )
                bot.send_message(
                    message.chat.id, "Список моих олимпиад:", reply_markup=markup
                )
            else:
                bot.send_message(message.chat.id, "Список пуст 😞")
        elif message.text == "Да":
            if selected_olympiad:
                flag = check_olympiad(selected_olympiad, check)
                if flag:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button_add = types.KeyboardButton("Добавить олимпиаду")
                    button_mine = types.KeyboardButton("Список добавленных олимпиад")
                    markup.add(button_add, button_mine)
                    bot.send_message(
                        message.chat.id,
                        "Олимпиада уже добавлена в список.",
                        reply_markup=markup,
                    )
                else:
                    add_olympiad(selected_olympiad, check)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button_add = types.KeyboardButton("Добавить олимпиаду")
                    button_mine = types.KeyboardButton("Список добавленных олимпиад")
                    markup.add(button_add, button_mine)
                    bot.send_message(
                        message.chat.id,
                        "Олимпиада добавлена в список 🥳",
                        reply_markup=markup,
                    )
        elif message.text == "Нет":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_add = types.KeyboardButton("Добавить олимпиаду")
            button_mine = types.KeyboardButton("Список добавленных олимпиад")
            markup.add(button_add, button_mine)
            bot.send_message(
                message.chat.id,
                "Попробуй выбрать другую олимпиаду",
                reply_markup=markup,
            )
        elif message.text == "Удалить":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_add = types.KeyboardButton("Добавить олимпиаду")
            button_mine = types.KeyboardButton("Список добавленных олимпиад")
            markup.add(button_add, button_mine)
            delete_olympiad(delete_ol, check)
            bot.send_message(
                message.chat.id, "Олимпиада удалена из списка", reply_markup=markup
            )
        elif message.text == "Оставить все как есть":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_add = types.KeyboardButton("Добавить олимпиаду")
            button_mine = types.KeyboardButton("Список добавленных олимпиад")
            markup.add(button_add, button_mine)
            bot.send_message(
                message.chat.id, "Сохранено без изменений", reply_markup=markup
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
            "Для начала нужно зарегистироваться или войти в аккаунт:",
            reply_markup=markup,
        )