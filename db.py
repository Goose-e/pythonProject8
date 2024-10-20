import psycopg
from psycopg_pool import AsyncConnectionPool
import idGenerator
from config import *

asyncConnectionPool = None



async def initialize_pool():
    global asyncConnectionPool
    asyncConnectionPool = AsyncConnectionPool(
        f"dbname={dbConst} user={user} password='{password}' host='{host}'",
        min_size=1,
        max_size=10,
    )
    await asyncConnectionPool.open()


class DaBa:
    def __init__(self):
        self.con = AsyncConnectionPool(
            f"dbname={dbConst} user={user} password='{password}' host='{host}'",
            min_size=1,
            max_size=10,
        )
        self.cur = self.con.cursor()

    def create_admin_table(self):
        self.cur.execute('DROP TABLE IF EXISTS "admin";')
        self.cur.execute("""
                    CREATE TABLE "admin" (
                        "admin_id" BIGINT NOT NULL PRIMARY KEY,
                        "admin_login" VARCHAR(20) NOT NULL UNIQUE,
                        "admin_password" VARCHAR(255) NOT NULL
                    );
                """)
        self.cur.execute("ALTER TABLE admin OWNER TO hackaton_admin;")
        self.cur.execute("GRANT ALL PRIVILEGES ON DATABASE Hackaton TO hackaton_admin;")
        self.con.commit()

    def add_admin(self, login, password):
        self.cur.execute(
            "INSERT INTO admin (admin_id, admin_login, admin_password) VALUES (%s, %s, %s)",
            (idGenerator.generationId(), login, password)
        )
        self.con.commit()

    def create_user_table(self):
        self.cur.execute(f"""
          DROP TABLE IF EXISTS {dbConst};
            CREATE TABLE user_info (
                user_info_id BIGINT NOT NULL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                secret_info VARCHAR
            );
        """)
        self.cur.execute("ALTER TABLE user_info OWNER TO hackaton_admin;")
        self.cur.execute("""
            GRANT DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE 
            ON user_info TO hackaton_admin;
        """)
        self.con.commit()


class UserManager:
    def __init__(self):
        self.con = psycopg.connect(
            dbname='postgres',  # Подключение к системной базе данных
            user='postgres',  # Имя суперпользователя
            password=f'{superUserPassword}',  # Пароль суперпользователя
            host='localhost'
        )
        self.cur = self.con.cursor()

    def create_user(self, username, user_password):
        self.cur.execute(f"DROP ROLE IF EXISTS {username};")
        self.cur.execute(f"CREATE ROLE {username} WITH LOGIN PASSWORD '{user_password}';")
        self.cur.execute(f"ALTER ROLE {username} CREATEDB;")
        self.con.commit()

    def grant_privileges(self, username, database):
        self.cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {username};")
        self.cur.execute(f"GRANT CREATE ON SCHEMA public TO {username};")
        self.con.commit()

    def create_database(self, database_name):
        self.cur.close()
        self.con.close()
        with psycopg.connect(
                dbname='postgres',
                user='postgres',
                password=f'{superUserPassword}',
                host='localhost', autocommit=True
        ) as temp_con:
            with temp_con.cursor() as temp_cur:
                temp_cur.execute(f"DROP DATABASE IF EXISTS  {database_name};")
                temp_cur.execute(f"CREATE DATABASE {database_name};")
                temp_con.commit()
        self.con = psycopg.connect(
            dbname=database_name,
            user='postgres',
            password=f'{superUserPassword}',
            host='localhost'
        )
        self.cur = self.con.cursor()


# Асинхронный метод для получения подключения
async def get_conn():
    conn = await asyncConnectionPool.getconn()
    return conn



if __name__ == "__main__":
    superUserPassword = "Kolos213"
    manager = UserManager()
    manager.create_database(f'{dbConst}')
    manager.create_user(f'{user}', f'{password}')
    manager.grant_privileges(f'{user}', f'{dbConst}')
    db = DaBa()
    db.create_admin_table()
    db.add_admin('admin_login', 'admin_password')
    db.create_user_table()
