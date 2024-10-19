import psycopg2
from config import *

try:
    connection = psycopg2.connect(
        host=host,  # Адрес сервера
        database=database,  # Название базы данных
        user=user,  # Имя пользователя PostgreSQL
        password=password  # Пароль пользователя
    )
    cursor = connection.cursor()

except Exception as ex:
    print(f"[INFO] Error while working: {ex}")
finally:
    if connection:
        connection.close()
        print("[INFO] connection closed")
