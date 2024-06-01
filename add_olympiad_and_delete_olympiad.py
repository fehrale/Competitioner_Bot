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
