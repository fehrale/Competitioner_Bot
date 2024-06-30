import telebot
import time
from telebot import types
import pickle
import sqlite3
import threading
from datetime import datetime, timedelta

bot = telebot.TeleBot("6661527759:AAGXDtVjWVPnhsBDVFFyP9DN_uzc5cCJno8")


def add_chatid(chat_id: int, login: str) -> str | None:
    """Добавляет chat_id в список chat_id, связанных с пользователем.

    Устанавливает соединение с базой данных, извлекает текущий список chat_id,
    добавляет новый chat_id, обновляет базу данных и закрывает соединение.
    """
    # Установливаем соединение с базой данных
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Извлекаем текущий массив login_chatids из базы данных
    cursor.execute("SELECT login_chatids FROM users WHERE username = ?", (login,))
    login_chatids = cursor.fetchone()[0]
    # Если массив login_chatids пуст, создаем новый массив
    if login_chatids is None:
        login_chatids = []
    else:
        # Преобразуем массив login_chatids из двоичного объекта в список Python
        login_chatids = pickle.loads(login_chatids)
    # Добавляем chat_id в список login_chatids
    login_chatids.append(chat_id)
    # Преобразуем список login_chatids обратно в двоичный объект
    login_chatids = pickle.dumps(login_chatids)
    # Обновляем поле login_chatids в базе данных
    cursor.execute(
        "UPDATE users SET login_chatids = ? WHERE username = ?", (login_chatids, login)
    )
    conn.commit()
    # Закрывем соединение с базой данных
    cursor.close()
    conn.close()


def check_logging(chat_id: int, login: str) -> bool:
    """
    Проверяет, зарегистрирован ли пользователь с данным логином в боте.

    Устанавливает соединение с базой данных, извлекает список идентификаторов чатов,
    связанных с пользователем, проверяет наличие chat_id в этом списке и отправляет
    сообщение с идентификаторами чатов пользователю. Возвращает True,
    если chat_id найден, и False, если нет.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT login_chatids FROM users WHERE username = ?", (login,))
    login_chatids = cursor.fetchone()[0]
    if login_chatids is None:
        return False
    else:
        login_chatids = pickle.loads(login_chatids)
    for i in login_chatids:
        bot.send_message(chat_id, f"{i}")
    return chat_id in login_chatids


def check_account(chat_id: int) -> str | None:
    """
    Проверяет, авторизован ли пользователь с данным chat_id в боте.

    Устанавливает соединение с базой данных, извлекает всех пользователей,
    проверяет наличие chat_id в списке идентификаторов чатов каждого пользователя
    и возвращает логин пользователя, если chat_id найден. Возвращает None, если chat_id
    не найден.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        login_chatids = user[3]
        if login_chatids is None:
            continue
        login_chatids = pickle.loads(login_chatids)
        if chat_id in login_chatids:
            return user[1]
    return None


def delete_id(chat_id: int, username: str) -> str | None:
    """
    Удаляет идентификатор чата из списка идентификаторов чатов, связанных с пользователем.

    Устанавливает соединение с базой данных, извлекает текущий список идентификаторов чатов,
    удаляет переданный идентификатор чата, обновляет базу данных и закрывает соединение.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT login_chatids FROM users WHERE username = ?", (username,))
    login_chatids = cursor.fetchone()[0]
    if login_chatids is None:
        return
    login_chatids = pickle.loads(login_chatids)
    login_chatids.remove(chat_id)
    login_chatids = pickle.dumps(login_chatids)
    cursor.execute(
        "UPDATE users SET login_chatids = ? WHERE username = ?",
        (login_chatids, username),
    )
    conn.commit()
    cursor.close()
    conn.close()


def add_olympiad(olymp: str, login: str) -> str | None:
    """
    Добавляет олимпиаду в список сохраненных олимпиад пользователя.

    Устанавливает соединение с базой данных, извлекает текущий список сохраненных олимпиад,
    добавляет переданную олимпиаду, обновляет базу данных и закрывает соединение.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saved_olymps FROM users WHERE username = ?", (login,))
    saved_olymps = cursor.fetchone()[0]
    if saved_olymps is None:
        saved_olymps = []
    else:
        saved_olymps = pickle.loads(saved_olymps)
    saved_olymps.append(olymp)
    saved_olymps = pickle.dumps(saved_olymps)
    cursor.execute(
        "UPDATE users SET saved_olymps = ? WHERE username = ?", (saved_olymps, login)
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_olympiad(olymp: str, username: str) -> str | None:
    """
    Удаляет олимпиаду из списка сохраненных олимпиад пользователя.

    Устанавливает соединение с базой данных, извлекает текущий список сохраненных олимпиад,
    удаляет переданную олимпиаду, обновляет базу данных и закрывает соединение.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saved_olymps FROM users WHERE username = ?", (username,))
    saved_olymps = cursor.fetchone()[0]
    if saved_olymps is None:
        return
    saved_olymps = pickle.loads(saved_olymps)
    saved_olymps.remove(olymp)
    saved_olymps = pickle.dumps(saved_olymps)
    cursor.execute(
        "UPDATE users SET saved_olymps = ? WHERE username = ?", (saved_olymps, username)
    )
    conn.commit()
    cursor.close()
    conn.close()


def save_olympiads(username: str) -> list:
    """
    Возвращает список сохраненных олимпиад пользователя.

    Устанавливает соединение с базой данных, извлекает список сохраненных олимпиад
    для данного пользователя и возвращает список олимпиад.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saved_olymps FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        return []
    else:
        return pickle.loads(result[0])


def check_olympiad(olymp: str, username: str) -> bool:
    """
    Проверяет, сохранена ли олимпиада пользователем.

    Устанавливает соединение с базой данных, извлекает список сохраненных олимпиад для данного пользователя и проверяет,
    содержит ли список переданную олимпиаду. Возвращает True, если олимпиада сохранена, и False, если нет.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT saved_olymps FROM users WHERE username=?""", (username,))
    saved_olymps_blob = cursor.fetchone()[0]
    if not saved_olymps_blob:
        return False
    else:
        saved_olymps = pickle.loads(saved_olymps_blob)
        return olymp in saved_olymps


@bot.message_handler(commands=["start"])
def start_message(message: types.Message) -> str | None:
    """
    Отправляет приветственное сообщение пользователю.

    В зависимости от того, зарегистрирован ли пользователь, отправляет приветственное сообщение,
    кнопки для входа или регистрации, либо кнопки для добавления или просмотра сохраненных олимпиад.
    """
    chat_id = message.chat.id
    # Проверяем выпролен ли вход в систему у пользователя или нет
    check = check_account(chat_id)
    if check:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(
            message.chat.id,
            "Привет👋, я Competitioner бот! Я помогу тебе с выбором олимпиады и напомню о ее начале в удобное время.",
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


# Функция для проверки учетных данных пользователя
def check_credentials(username: str, password: str) -> bool:
    """
    Проверяет учетные данные пользователя.

    Устанавливает соединение с базой данных, выполняет запрос для поиска пользователя с указанными учетными данными и
    возвращает True, если пользователь найден, и False, если не найден.
    """
    # Выполняем запрос к базе данных для поиска пользователя с указанными учетными данными
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
    )
    result = cursor.fetchone()
    conn.commit()
    # Если пользователь найден, верните его идентификатор
    if result:
        return True
    # Если пользователь не найден, верните None
    else:
        return False


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


if __name__ == "__main__":
    # Создаем таблицу пользователей, если она еще не существует
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, login_chatids BLOB, saved_olymps BLOB)"""
    )
    conn.commit()

    olympics = {
        "ФизТех": "главная олимпиада для всех желающих поступать в МФТИ, а также одна из основных олимпиад для абитуриентов Высшей школы экономики и МГУ.\nУровень олимпиады: I\nНачало олимпиады: 20.09.24",
        "Ломоносов": "Ежегодная олимпиада школьников, проводимая МГУ совместно с другими вузами России. Включена в Перечень олимпиад школьников, что дает право поступления без вступительных испытаний в вузы России.\nУровень олимпиады: I\nНачало олимпиады: 15.10.24",
        "МежВед": "Межрегиональная олимпиада школьников на базе ведомственных образовательных организаций проводится Академией ФСБ России и Академией ФСО России для учащихся 9–11 классов.\nУровень олимпиады: II\nНачало олимпиады: 08.10.24",
        "Крипта": "Единственная международная олимпиада по криптографии для студентов, школьников и профессионалов.\nУровень олимпиады: II\nНачало олимпиады: 10.11.24",
        "Будущее науки": "Региональная олимпиада по математике и физике. Проводится для школьников 7–11 классов.\nУровень олимпиады: III\nНачало олимпиады: 15.11.24",
    }

    user_wait_times = {}
    selected_olympiad = None
    delete_ol = None
    username = ""

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=0)
        except:
            time.sleep(10)
