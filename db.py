import asyncio

import psycopg
from psycopg_pool import AsyncConnectionPool

import models.Admin
from consts import *
from models.Admin import Admin
from models.Regular import Regular
from models.UserInfo import UserInfo

superUserPassword = "Kolos213"
asyncConnectionPool = None

async def close_pool():
    global asyncConnectionPool


async def initialize_pool():
    global asyncConnectionPool
    try:
        asyncConnectionPool = AsyncConnectionPool(
            f"dbname=hackaton user=hackaton_admin password='admin' host='localhost'",
            min_size=1,
            max_size=10,
        )
        print(type(asyncConnectionPool))  # Должно быть <class '...'>
        await asyncConnectionPool.open()
        print("pool is open")
        # Попробуем открыть пул
    except Exception as e:
        print(f"Ошибка при инициализации пула: {e}")


class DaBa:
    def __init__(self):
        self.con = asyncConnectionPool

    async def create_admin_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "admin";')
                await cur.execute("""
                          CREATE TABLE "admin_table" (
                              "admin_id" serial PRIMARY KEY,
                              "admin_login" VARCHAR(20) NOT NULL UNIQUE,
                              "admin_password" VARCHAR(255) NOT NULL
                          );
                      """)
                await cur.execute("ALTER TABLE admin_table OWNER TO hackaton_admin;")
                await cur.execute("GRANT ALL PRIVILEGES ON DATABASE hackaton TO hackaton_admin;")
                await conn.commit()

    async def add_admin(self, login, password):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO admin_table (admin_login, admin_password) VALUES (%s, %s)",
                    (login, password)
                )
                await conn.commit()

    async def create_full_user_table(self):

        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "full_user";')
                await cur.execute("""
                      CREATE TABLE "full_user" (
                          "user_id" int PRIMARY KEY,
                          "email" VARCHAR,
                          "login" VARCHAR,
                          "support_level" INT ,
                          "age" INT,
                          "birthdate" DATE,
                          "first_name" VARCHAR,
                          "phone_number" VARCHAR,
                          "middle_name" VARCHAR,
                          "gender" VARCHAR,
                          "last_name" VARCHAR
                      );
                  """)
                await cur.execute("ALTER TABLE full_user OWNER TO hackaton_admin;")
                await conn.commit()

    async def create_user_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DROP TABLE IF EXISTS user_info;")
                await cur.execute("""CREATE TABLE user_info (
                    user_info_id serial PRIMARY KEY,
                    FOREIGN KEY  user_id  REFERENCES full_user ON DELETE CASCADE,
                    secret_info VARCHAR,
                    "endpoint" VARCHAR ,
                    "timestamp" TIMESTAMP
                );""")
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
                    await cursor.execute("SELECT user_id FROM user_info ")  # Замените на ваш запрос
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)

            return

    async def getAllUserInfo(self):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT user_id, secret_info FROM user_info ")
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
                        f"SELECT user_id, secret_info FROM user_info WHERE user_id ={id}")
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
                    await cursor.execute(
                        "SELECT admin_login, admin_password FROM admin_table")  # Замените на ваш запрос
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
                        "SELECT * FROM admin_table WHERE admin_login = %s AND admin_password = %s",
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
            async with self.con.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO public.admin_table (admin_login, admin_password) VALUES (%s, %s)",
                        (admin.adminLogin, admin.adminPassword)
                    )
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
                        "regular_expression" VARCHAR NOT NULL,
                        "expression_status" INT NOT NULL
                    );
                """)
                await cur.execute("ALTER TABLE regular OWNER TO hackaton_admin;")
                await cur.execute("GRANT ALL PRIVILEGES ON DATABASE hackaton TO hackaton_admin;")
                await conn.commit()

    async def saveInfoInRegular(self, regular_expression):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO public.regular (regular_expression, expression_status) VALUES (%s, %s)",
                        (regular_expression, 1)
                    )
                    result = "Данные сохранены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def deleteRegular(self, regular_expression_id):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "DELETE FROM public.regular WHERE regular_id = %s",
                        (regular_expression_id,)
                    )
                    result = "Данные удалены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def getAllRegulars(self):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "SELECT * FROM public.regular ORDER BY regular_id"
                    )
                rows = await cursor.fetchall()
                result = [Regular(regular_id=row['regular_id'],
                                  regular_expression=row['regular_expression'],
                                  expression_status=row['expression_status']) for row in rows]
                return result
        except Exception as ex:
            print(f"Error: ", ex)
        return

    async def changeRegularStatus(self, regular_expression_id, expression_status):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "UPDATE regular SET expression_status = %s WHERE regular_id = %s",
                        (expression_status, regular_expression_id)
                    )
                    result = "Данные изменены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def create_source_reader_table(self):

        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "source";')
                await cur.execute("""
                          CREATE TABLE "source" (
                              "source_id" serial PRIMARY KEY,
                              "source_adress" VARCHAR NOT NULL,
                              "source_status" INT NOT NULL
                          );
                      """)
                await cur.execute("ALTER TABLE source OWNER TO hackaton_admin;")
                await conn.commit()


# нужны апдейты статусов для сурс и регулярок
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
            dbname=f'postgres',  # Подключение к системной базе данных
            user='postgres',  # Имя суперпользователя
            password=f'{superUserPassword}',  # Пароль суперпользователя
            host=f'localhost'
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
                host=f'localhost',
                autocommit=True
        ) as temp_con:
            with temp_con.cursor() as temp_cur:
                temp_cur.execute(f"DROP DATABASE IF EXISTS  {database_name};")
                temp_cur.execute(f"CREATE DATABASE {database_name};")
                temp_con.commit()
        self.con = psycopg.connect(
            dbname=database_name,
            user='postgres',
            password=f'{superUserPassword}',
            host=f'localhost'
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
    await db.create_regular_expressions_table()
    await db.create_source_reader_table()
    await db.create_full_user_table()
    await db.add_admin('gol', '123')


async def test_db_connection():
    try:
        async with await get_conn() as conn:
            print("Connected to the database successfully.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
def DaBa1():
    return DaBa()

async def main():
    await initialize_pool()  # Инициализируйте пул соединений
    await test_db_connection()  # Тест подключения к базе данных
    data = DaBa()
    print(type(data.con))


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(main())  # Запустите основную асинхронную функцию
    manager = UserManager()
    manager.create_database(f'{dbConst}')
    manager.create_user(f'{user}', f'{password}')
    manager.grant_privileges(f'{user}', f'{dbConst}')
    asyncio.run(adCreate())
