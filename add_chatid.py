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
