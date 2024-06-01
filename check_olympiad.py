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
