@bot.message_handler(commands=["n"])
def start_message(message: telebot.types.Message) -> None:
    """
    Обрабатывает команду '/n'.

    Если у пользователя есть существующая учетная запись, запрашивает количество дней, через 
    которое нужно отправить сообщение со ссылками для регистрации на олимпиады. Если у 
    пользователя нет существующей учетной записи, предоставляет встроенную клавиатуру 
    с опциями входа в систему или регистрации.
    """
    chat_id = message.chat.id
    check = check_account(chat_id)
    if check:
        msg = bot.send_message(
            chat_id,
            "Через сколько дней прислать сообщение с ссылками для регистрации на олимпиады?",
        )
        bot.register_next_step_handler(msg, process_days)
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
            chat_id,
            "Привет👋, я Competitioner бот! Я помогу тебе с выбором олимпиады и напомню о ее начале в удобное время.\nНажми на одну из появившихся кнопок:",
            reply_markup=markup,
        )


def process_days(message: telebot.types.Message) -> None:
    """
    Обрабатывает введенное пользователем количество дней.

    Пытается преобразовать введенное значение в целое число. Если преобразование выполнено 
    успешно, сохраняет время ожидания пользователя в словаре `user_wait_times` и отправляет 
    сообщение с указанием, что бот пришлет ссылки на регистрацию через указанное количество 
    дней. Затем запускает поток для ожидания и отправки ссылок.

    Если преобразование в целое число не удалось, отправляет сообщение с просьбой ввести 
    корректное число.
    """

    try:
        chat_id = message.chat.id
        days = int(message.text)
        user_wait_times[chat_id] = datetime.now() + timedelta(days=days)
        bot.send_message(chat_id, "Хорошо, жди сообщения 😌")
        threading.Thread(target=wait_and_send_links, args=(chat_id, days)).start()
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введи корректное число")


def wait_and_send_links(chat_id: int, days: int) -> None:
    """
    Ожидает указанное количество дней и отправляет пользователю ссылки для регистрации на олимпиады.
    """
    time.sleep(days * 24 * 60 * 60)
    bot.send_message(chat_id, "Вот ссылки для регистрации на олимпиады: [ссылки]")