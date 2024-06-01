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
