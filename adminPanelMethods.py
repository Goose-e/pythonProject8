from db import DaBa
import asyncio
import httpx
from consts import portS1, portS2, portS3


class adminControl():
    @staticmethod
    async def changeMaskMethod(maskMethodType):
        async with httpx.AsyncClient() as client:
            data = {"Message": ''}
            response = await client.post(f"http://127.0.0.1:{portS1}/proxy/", json=(data, maskMethodType))
            print(f"Ответ от proxy: {response.status_code}, {response.text}")
            response = await client.post(f"http://127.0.0.1:{portS2}/proxy/", json=(data, maskMethodType))
            print(f"Ответ от proxy: {response.status_code}, {response.text}")
            response = await client.post(f"http://127.0.0.1:{portS3}/proxy/", json=(data, maskMethodType))
            print(f"Ответ от proxy: {response.status_code}, {response.text}")


@staticmethod
async def addRegularExpression(Expression):
    await asyncio.to_thread(DaBa().saveInfoInRegular, Expression)


@staticmethod
async def addReaderSource(sourceAdress):
    pass
    await asyncio.to_thread(DaBa().saveSource, sourceAdress)
