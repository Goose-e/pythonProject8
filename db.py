from csv import excel

import psycopg2


def connectToDb():
    try:
        connection = psycopg2.connect(
            host="localhost",  # Адрес сервера
            database="Hackaton",  # Название базы данных
            user="hackaton_admin",  # Имя пользователя PostgreSQL
            password="hackaton"  # Пароль пользователя
        )
    except:
        print("error")

