import asyncio

import psycopg
from psycopg_pool import AsyncConnectionPool

import models.Admin
from consts import *
from models.Admin import Admin
from models.FullUser import FullUser
from models.Regular import Regular
from models.UserInfo import UserInfo

superUserPassword = "Kolos213"
asyncConnectionPool = None


async def close_pool():
    global asyncConnectionPool
    # if asyncConnectionPool:
    #     # await asyncConnectionPool.close()


async def initialize_pool():
    global asyncConnectionPool
    try:
        asyncConnectionPool = AsyncConnectionPool(
            f"dbname=hackaton user=hackaton_admin password='admin' host='127.0.0.1'",
            min_size=1,
            max_size=1000,
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
                          "user_id" BIGINT  PRIMARY KEY,
                          "email" VARCHAR,
                          "login" VARCHAR,
                          "support_level" varchar ,
                          "age" INT,
                          "birthdate" DATE,
                          "first_name" VARCHAR,
                          "phone_number" VARCHAR,
                          "second_name" VARCHAR,
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
                    user_id BIGINT  not null, 
                     FOREIGN KEY  (user_id)  REFERENCES full_user(user_id) ON DELETE CASCADE,
                    secret_info VARCHAR,
                    endpoint_place VARCHAR ,
                    message_time TIMESTAMP
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

    async def findUserInfoByUserId(self, id):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT user_id, secret_info,endpoint_place,message_time FROM user_info WHERE user_id ={id}")
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def findUserByUserId(self, id):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT * FROM full_user WHERE user_id ={id}")
                    result = await cursor.fetchone()
                    if result:
                        user = FullUser(
                            user_id=result[0],
                            email=result[1],
                            login=result[2],
                            support_level=result[3],
                            age=result[4],
                            birthdate=result[5],
                            first_name=result[6],
                            phone_number=result[7],
                            second_name=result[8],
                            gender=result[9],
                            last_name=result[10],
                        )
                        return user
                    else:
                        return None
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def saveFullUser(self, user: FullUser):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO full_user ( user_id, email, login, support_level, age, birthdate,first_name, phone_number, second_name, gender, last_name)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            user.user_id, user.email, user.login, user.support_level, user.age,
                            user.birthdate, user.first_name, user.phone_number, user.second_name,
                            user.gender, user.last_name
                        )
                    )
                    result = "Данные сохранены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def saveInfoInDB(self, userInfo):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO public.user_info (user_id, secret_info,endpoint_place,message_time) VALUES (%s, %s, %s, TO_TIMESTAMP(%s))",
                        (userInfo.userId, userInfo.secretInfo, userInfo.endpoint, userInfo.timestamp)
                    )
                    result = "Данные сохранены"
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return

    async def getAdmin(self, login, password):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT * FROM admin_table WHERE admin_login = %s and admin_password = %s",
                        (login, password))  # Замените на ваш запрос
                    result = await cursor.fetchall()
                    return result
        except Exception as ex:
            print(f"Error: ", ex)
            return False

    async def getUserByID(self, login):
        try:
            async with await get_conn() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT * FROM admin_table WHERE admin_login = %s", (login,))
                    result = await cursor.fetchall()
                    print(result)
                    return result
        except Exception as ex:
            print(f"Error: {ex}")
            return False

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
            return False

    async def getAdminFromDB(self, adminLogin, adminPassword):
        try:
            async with self.con.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT * FROM admin_table WHERE admin_login = %s AND admin_password = %s",
                        (adminLogin, adminPassword)
                    )
                    result = await cur.fetchone()
                    if result:
                        admin = Admin(adminId=result[0], adminLogin=result[1], adminPassword=result[2])
                        return admin
                    else:
                        return None
        except Exception as ex:
            print(f"Error: {ex}")
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
            # Получение нового соединения из пула
            async with self.con.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT * FROM regular ORDER BY regular_id")
                    rows = await cursor.fetchall()

                    # Преобразование строк результата в объекты
                    result = [Regular(regular_id=row[0],  # Убедитесь, что индексы правильные
                                      regular_expression=row[1],
                                      expression_status=row[2])
                              for row in rows]

                    return result
        except Exception as ex:
            print(f"Error: {ex}")
            return None

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
    conn = await asyncConnectionPool.getconn()
    return conn


async def release_conn(conn):
    await asyncConnectionPool.putconn(conn)


async def adCreate():
    await initialize_pool()
    db = DaBa()
    await db.create_admin_table()
    await db.add_admin('admin', 'admin')
    await db.create_regular_expressions_table()
    await db.create_source_reader_table()
    await db.create_full_user_table()
    await db.add_admin('gol', '123')
    await db.create_user_table()
    await db.create_regular_expressions_table()


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
    str = r'r"""(?<!\w)(\+?\d{1,3}[-\s]?)?\(?\d{2,4}\)?[-\s]?\d{1,3}[-\s]?\d{1,2}[-\s]?\d{2,3}(?!\w)"""'
    await data.saveInfoInRegular(str)
    str = r'r"""\b\d{4}[-\s]?\d{6}\b|\b[A-Z]{2}\d{7}\b"""'
    await data.saveInfoInRegular(str)
    str = r'r"""(?<!\w)(?:\d{4}[-\s]?){3}\d{4}\b|\d{16}\b"""'
    await data.saveInfoInRegular(str)
    # номер счёта
    str = r'r"""(?<!\w)(?:\d{4}[-\s]?){4}\d{4}\b"""'
    # даты рождения
    await data.saveInfoInRegular(str)
    str = r'r"""(\b\d{2}[-./]\d{2}[-./]\d{4}\b)|(\b\d{4}[-./]\d{2}[-./]\d{2}\b)|(\b\d{2}\s\w{3,}\s\d{4}\b)"""'
    await data.saveInfoInRegular(str)
    str = r'r"""(?<!\w)(\b[A-ZА-ЯЁ][a-zа-яё]+\s[A-ZА-ЯЁ][a-zа-яё]+\b)|(\b[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ][a-zа-яё]+\b)|(\b[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ][a-zа-яё]+\b)"""'
    # Адреса
    await data.saveInfoInRegular(str)
    str = r'r"""(?<!\w)(Россия|Беларусь+|г\.\s?[А-Яа-яЁё]+|г\.[-]?\s?[А-Яа-яЁё]+|город\s?[А-Яа-яЁё]+|ул\.\s?[А-Яа-яЁё]+|улица\s?[А-Яа-яЁё]+|пер\.\s?[А-Яа-яЁё]+|[А-Яа-яЁё]+[-\s]?пер\.|переулок\s?[А-Яа-яЁё]+|д\.-?\s?\d+|дом\s?\d+|кв\.-?\s?\d+|квартира\s?\d+)"""'
    await data.saveInfoInRegular(str)
    str = r'r"""(?<!\w)\d{2}[-\s]?\d{3}[-\s]?\d{3}(?!\w)"""'
    await data.saveInfoInRegular(str)
    str = r'r"""(?<!\w)ДК[-\s]?\d{8}\b|[А-Я]{2}[-\s]?\d{8}\b"""'
    await data.saveInfoInRegular(str)
    all = await data.getAllRegulars()

    print(all)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(main())  # Запустите основную асинхронную функцию

    manager = UserManager()
    manager.create_database(f'{dbConst}')
    manager.create_user(f'{user}', f'{password}')
    manager.grant_privileges(f'{user}', f'{dbConst}')
    asyncio.run(adCreate())
