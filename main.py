import telebot
import time
from telebot import types
import pickle
import sqlite3
import threading
from datetime import datetime, timedelta

bot = telebot.TeleBot("6661527759:AAGXDtVjWVPnhsBDVFFyP9DN_uzc5cCJno8")


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
