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
