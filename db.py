import asyncio

import psycopg
from psycopg_pool import AsyncConnectionPool
import models.Admin
from consts import *
from models.Admin import Admin
from models.UserInfo import UserInfo

asyncConnectionPool = None


async def close_pool():
    global asyncConnectionPool
    await asyncConnectionPool.close()


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
        self.con = asyncConnectionPool

    async def create_admin_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "admin";')
                await cur.execute("""
                          CREATE TABLE "admin" (
                              "admin_id" serial PRIMARY KEY,
                              "admin_login" VARCHAR(20) NOT NULL UNIQUE,
                              "admin_password" VARCHAR(255) NOT NULL
                          );
                      """)
                await cur.execute("ALTER TABLE admin OWNER TO hackaton_admin;")
                await cur.execute("GRANT ALL PRIVILEGES ON DATABASE hackaton TO hackaton_admin;")
                await conn.commit()

    async def add_admin(self, login, password):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO admin (admin_login, admin_password) VALUES (%s, %s)",
                    (login, password)
                )
                await conn.commit()

    async def create_user_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    DROP TABLE IF EXISTS user_info;
                    CREATE TABLE user_info (
                        user_info_id serial PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        secret_info VARCHAR
                    );
                """)
                await cur.execute("ALTER TABLE user_info OWNER TO hackaton_admin;")
                await cur.execute("""
                    GRANT DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE 
                    ON user_info TO hackaton_admin;
                """)
                await conn.commit()

    async def getAllUsers(self):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT u.user_id FROM user_info u")  # Замените на ваш запрос
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)

            return

    async def getAllUserInfo(self):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT u.user_id, u.secret_info FROM user_info u")
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def findUserById(self, id):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT u.user_id, u.secret_info FROM user_info u WHERE user_id ={id}")
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def saveInfoInDB(self, userId, secretInfo):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO public.user_info (user_id, secret_info) VALUES (%s, %s)",
                        (userId, secretInfo)
                    )
                    result = "Данные сохранены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def getAllAdmins(self):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT a.admin_login FROM admin a")  # Замените на ваш запрос
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)

            return

    async def authAdmin(self, admin: models.Admin.Admin):
        try:
            async with self.con.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT * FROM admin a WHERE admin_login = %s AND admin_password = %s",
                        (admin.adminLogin, admin.adminPassword)
                    )
                    result = await cur.fetchone()
                    if result:
                        admin = Admin(adminId=result[0], adminLogin=result[1], adminPassword=result[2])
                        return admin
                    else:
                        return None
        except Exception as ex:
            print(f"Error: ", ex)
            return None

    async def saveAdminInDB(self, admin: models.Admin.Admin):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"INSERT INTO public.admin (admin_login, admin_password) VALUES ({admin.adminLogin},{admin.adminPassword})")
                    result = "Данные сохранены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def create_regular_expressions_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "regular";')
                await cur.execute("""
                          CREATE TABLE "regular" (
                              "regular_id" serial PRIMARY KEY,
                              "regular_exspression" VARCHAR(255) NOT NULL,
                              "expression_status" INT NOT NULL
                          );
                      """)
                await cur.execute("ALTER TABLE regular OWNER TO hackaton_admin;")
                await cur.execute("GRANT ALL PRIVILEGES ON DATABASE hackaton TO hackaton_admin;")
                await conn.commit()

    async def saveInfoInRegular(self, regular_exspression):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO public.regular (regular_exspression, expression_status) VALUES (%s, %s)",
                        (regular_exspression, 1)
                    )
                    result = "Данные сохранены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def create_source_reader_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "source";')
                await cur.execute("""
                          CREATE TABLE "regular" (
                              "source_id" serial PRIMARY KEY,
                              "source_adress" VARCHAR(255) NOT NULL,
                              "source_status" INT NOT NULL
                          );
                      """)
                await cur.execute("ALTER TABLE regular OWNER TO hackaton_admin;")
                await cur.execute("GRANT ALL PRIVILEGES ON DATABASE hackaton TO hackaton_admin;")
                await conn.commit()
#нужны апдейты статусов для сурс и регулярок
    async def saveInfoInSource(self, source):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO public.source (source_adress, source_status) VALUES (%s, %s)",
                        (source, 1)
                    )
                    result = "Данные сохранены"
                    return result

        except Exception as ex:
            print(f"Error: ", ex)
            return

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
    return await asyncConnectionPool.getconn()


async def adCreate():
    await initialize_pool()
    db = DaBa()
    await db.create_admin_table()
    await db.add_admin('admin', 'admin')
    await db.create_user_table()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    superUserPassword = "Kolos213"
    manager = UserManager()
    manager.create_database(f'{dbConst}')
    manager.create_user(f'{user}', f'{password}')
    manager.grant_privileges(f'{user}', f'{dbConst}')
    asyncio.run(adCreate())
