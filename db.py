from functools import lru_cache
import psycopg
import asyncio
from psycopg_pool import AsyncConnectionPool, ConnectionPool
from config import *

asyncConnectionPool = None


async def initialize_pool():
    global asyncConnectionPool

    # Подключаемся как суперпользователь (например, postgres) для создания пользователя и базы данных
    superuser_conn = psycopg.connect(
        dbname=f'{database}',
        user=f'{user}',  # Укажите имя пользователя с правами суперпользователя
        password=f'{password}',  # Укажите пароль суперпользователя
        host='localhost'
    )

    try:
        with superuser_conn.cursor() as cursor:
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'hackaton_admin') THEN
                        CREATE ROLE hackaton_admin WITH LOGIN PASSWORD 'ваш_пароль';
                        ALTER ROLE hackaton_admin CREATEDB;
                    END IF;
                END $$;
            """)
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'Hackaton') THEN
                        CREATE DATABASE "Hackaton"
                        WITH
                        OWNER = hackaton_admin
                        ENCODING = 'UTF8'
                        LC_COLLATE = 'English_United States.1252'
                        LC_CTYPE = 'English_United States.1252'
                        TABLESPACE = pg_default
                        CONNECTION LIMIT = -1
                        IS_TEMPLATE = False;
                    END IF;
                END $$;
            """)

    finally:
        superuser_conn.close()

    # Подключаемся к созданной базе данных как hackaton_admin
    asyncConnectionPool = AsyncConnectionPool(
        f"dbname={database} user={user} password='{password}' host='{host}'",
        min_size=1,
        max_size=10,
    )
    await asyncConnectionPool.open()


async def get_conn():
    conn = await asyncConnectionPool.getconn()
    return conn
