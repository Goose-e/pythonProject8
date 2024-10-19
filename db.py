from functools import lru_cache

import psycopg
import asyncio
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from config import *

asyncConnectionPool = None


async def initialize_pool():
    global asyncConnectionPool
    asyncConnectionPool = AsyncConnectionPool(
        f"dbname={database} user={user} password={password} host={host}",
        min_size=1,
        max_size=10,
    )
    await asyncConnectionPool.open()


async def get_conn():
    conn = await asyncConnectionPool.getconn()
    return conn
