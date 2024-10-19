from logging import exception

from db import get_conn


async def fetch_data():
    try:
        async with await get_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM user_info")  # Замените на ваш запрос
                result = await cursor.fetchall()
                return result
    except Exception as ex:
        print(f"Error: ",ex)
        return