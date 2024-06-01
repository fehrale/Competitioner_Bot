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
