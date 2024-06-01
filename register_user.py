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
