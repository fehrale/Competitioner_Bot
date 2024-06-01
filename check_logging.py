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
