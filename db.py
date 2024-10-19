from functools import lru_cache
import psycopg
import asyncio
from psycopg_pool import AsyncConnectionPool

import idGenerator
from config import *

asyncConnectionPool = None


async def initialize_pool():
    global asyncConnectionPool

    asyncConnectionPool = AsyncConnectionPool(
        f"dbname={database} user={user} password='{password}' host='{host}'",
        min_size=1,
        max_size=10,
    )
    await asyncConnectionPool.open()


class DaBa():
    def __init__(self):
        self.con = psycopg.connect(
            dbname=database,
            user=user,  # Укажите имя пользователя с правами суперпользователя
            password=password,  # Укажите пароль суперпользователя
            host=host
        )
        self.cur = self.con.cursor()

    def create_user(self, username, user_password):
        # Создание пользователя с указанным паролем
        self.cur.execute(f"CREATE USER {username} WITH PASSWORD '{user_password}';")
        # Предоставление прав на создание баз данных
        self.cur.execute(f"ALTER USER {username} CREATEDB;")
        self.con.commit()

    def grant_privileges(self, username, database):
        # Назначение всех прав пользователю на указанную базу данных
        self.cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {username};")
        self.con.commit()

    def createTableUser(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_info (
                user_info_id BIGINT NOT NULL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                secret_info VARCHAR
            );
            """
        )
        self.cur.execute("ALTER TABLE user_info OWNER TO hackaton_admin;")
        self.cur.execute(
            "GRANT DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON user_info TO hackaton_admin;"
        )
        self.con.commit()

    def createAdmin(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS admin (
                admin_id       BIGINT NOT NULL PRIMARY KEY,
                admin_login    VARCHAR(20) NOT NULL UNIQUE,
                admin_password VARCHAR(255) NOT NULL
            );
            """
        )
        self.cur.execute("ALTER TABLE admin OWNER TO hackaton_admin;")
        self.cur.execute("GRANT ALL PRIVILEGES ON DATABASE Hackaton TO hackaton_admin;")
        self.con.commit()

    # Метод добавления админа
    def addAdmin(self, login, password):
        self.cur.execute(
            "INSERT INTO Admin (admin_id, admin_login, admin_password) VALUES (%s, %s, %s)",
            (idGenerator.generationId(), login, password)
        )
        self.con.commit()


class UserManager():
    def __init__(self):
        # Подключение от имени суперпользователя
        self.con = psycopg.connect(
            dbname=database,  # Подключение к системной базе данных, чтобы управлять пользователями
            user='postgres',  # Укажите имя суперпользователя
            password='Kolos213',  # Укажите пароль суперпользователя
            host='localhost'
        )
        self.cur = self.con.cursor()

    def create_user(self, username, user_password):
        # Создание пользователя с указанным паролем
        self.cur.execute(f"CREATE USER {username} WITH PASSWORD '{user_password}';")
        # Предоставление прав на создание баз данных
        self.cur.execute(f"ALTER USER {username} CREATEDB;")
        self.con.commit()

    def grant_privileges(self, username, database):
        # Назначение всех прав пользователю на указанную базу данных
        self.cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {username};")
        self.con.commit()

# Асинхронный метод для получения подключения
async def get_conn():
    conn = await asyncConnectionPool.getconn()
    return conn

if __name__ == "__main__":
    manager = UserManager()
    manager.create_user('hackaton_admin', 'ваш_пароль')
    manager.grant_privileges('hackaton_admin', 'Hackaton')
    DaBa().createAdmin()
    DaBa().AddAdmin("admin", "admin")
    DaBa().createTableUser()
import psycopg


# Пример использования
if __name__ == "__main__":
    manager = UserManager()
    manager.create_user('hackaton_admin', 'ваш_пароль')
    manager.grant_privileges('hackaton_admin', 'Hackaton')
