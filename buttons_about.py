@bot.message_handler(commands=["about"])
def start_message(message: telebot.types.Message) -> None:
    """Обрабатывает команду '/about'.

    Предоставляет информацию о боте и его функциональности новым пользователям. 
    Если у пользователя есть существующая учетная запись, предоставляет настраиваемую 
    раскладку клавиатуры с опциями добавления или просмотра списка олимпиад. Если у 
    пользователя нет существующей учетной записи, предоставляет встроенную 
    клавиатуру с опциями входа в систему или регистрации.
    """
    chat_id = message.chat.id
    check = check_account(chat_id)
    if check:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(
            message.chat.id,
            "Привет👋, я Competitioner бот! Я помогу тебе с выбором олимпиады и напомню о ее начале в удобное время",
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
            "Привет👋, я Competitioner бот! Я помогу тебе с выбором олимпиады и напомню о ее начале в удобное время.\nНажми на одну из появившихся кнопок:",
            reply_markup=markup,
        )
