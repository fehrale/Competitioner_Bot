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
