import psycopg
from psycopg_pool import AsyncConnectionPool
import idGenerator
import models.Admin
from consts import *
from models.Admin import Admin

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
        self.con = asyncConnectionPool

    async def create_admin_table(self):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DROP TABLE IF EXISTS "admin";')
                await cur.execute("""
                       CREATE TABLE "admin" (
                           "admin_id" BIGINT NOT NULL PRIMARY KEY,
                           "admin_login" VARCHAR(20) NOT NULL UNIQUE,
                           "admin_password" VARCHAR(255) NOT NULL
                       );
                   """)
                await cur.execute("ALTER TABLE admin OWNER TO hackaton_admin;")
                await cur.execute("GRANT ALL PRIVILEGES ON DATABASE Hackaton TO hackaton_admin;")
                await conn.commit()

    async def add_admin(self, login, password):
        async with self.con.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO admin (admin_id, admin_login, admin_password) VALUES (%s, %s, %s)",
                    (idGenerator.generationId(), login, password)
                )
                await conn.commit()

    async def create_user_table(self):
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
                        f"INSERT INTO public.user_info (user_info_id, user_id, secret_info) VALUES ({idGenerator.generationId()},{userId},{secretInfo})")
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

    async def authAdmin(self, login, password):
        try:
            async with self.con.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT * FROM admin a WHERE admin_login = %s AND admin_password = %s", (login, password)
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
                        f"INSERT INTO public.admin (admin_id, admin_login, admin_password) VALUES ({idGenerator.generationId()},{admin.adminLogin},{admin.adminPassword})")
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
    db = DaBa()
    await db.create_admin_table()
    await db.add_admin('admin_login', 'admin_password')
    await db.create_user_table()


if __name__ == "__main__":
    superUserPassword = "Kolos213"
    manager = UserManager()
    manager.create_database(f'{dbConst}')
    manager.create_user(f'{user}', f'{password}')
    manager.grant_privileges(f'{user}', f'{dbConst}')
