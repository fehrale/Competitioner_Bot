@bot.message_handler(commands=["exit"])
def start_message(message: telebot.types.Message) -> None:
    """
    Обрабатывает команду '/exit'. Предоставляет информацию о боте и его функциональности.
    """
    chat_id = message.chat.id
    check = check_account(chat_id)
    markup = types.InlineKeyboardMarkup()
    button_log = types.InlineKeyboardButton(
        text="Вход в систему", callback_data="login"
    )
    button_reg = types.InlineKeyboardButton(
        text="Регистрация в системе", callback_data="reg"
    )
    markup.add(button_log, button_reg)
    if check:
        delete_id(chat_id, check)
        bot.send_message(
            message.chat.id, f"{check}, ты вышел из аккаунта", reply_markup=markup
        )
    else:
        bot.send_message(
            message.chat.id, "Для начала зайди в свой аккаунт", reply_markup=markup
        )