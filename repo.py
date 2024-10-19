from db import get_conn
from idGenerator import generationId


async def getAllUsers():
    try:
        async with await get_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT u.user_id FROM user_info u")  # Замените на ваш запрос
                result = await cursor.fetchall()
                return result
    except Exception as ex:
        print(f"Error: ", ex)

        return


async def getUserInfo():
    try:
        async with await get_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT u.user_id, u.secret_info FROM user_info u")
                result = await cursor.fetchall()
                return result
    except Exception as ex:
        print(f"Error: ", ex)
        return


async def findUserById(id):
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

async def saveInfoInDB(userId,secretInfo):
    try:
        async with await get_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"INSERT INTO public.user_info (user_info_id, user_id, secret_info) VALUES ({generationId()},{userId},{secretInfo})")
                result = "Данные сохранены"
                return result
    except Exception as ex:
        print(f"Error: ", ex)
        return