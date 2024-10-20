import asyncio
import base64
from asyncio import WindowsSelectorEventLoopPolicy
from contextlib import asynccontextmanager

import rsa
from fastapi import FastAPI, Request
from Cryptodome.Cipher import AES

import httpx
import json
import uvicorn
import consts
import db
from consts import portS3, portC1
from maskMethods import Masking

from db import  DaBa

servApp = FastAPI()



async def lifespan(scope, receive, send):
    if scope['type'] == 'lifespan':
        global dataBase
        await db.initialize_pool()
        dataBase = DaBa()
        await send({"type": "lifespan.startup.complete"})  # Сообщаем о завершении старта
        try:
            while True:
                message = await receive()
                if message['type'] == 'lifespan.shutdown':
                    break
        finally:
            await db.close_pool()
            await send({"type": "lifespan.shutdown.complete"})  # Сообщаем о завершении остановки


servApp.router.lifespan = lifespan

(publicKey, privateKey) = rsa.newkeys(2048)


@servApp.get("/getPublicKey")
async def get_public_key():
    publicKeyUnmade = publicKey.save_pkcs1(format='PEM')
    return {"public_key": publicKeyUnmade.decode('utf-8')}


async def saveInfoInDB(userData):
    try:
        result = await dataBase.saveInfoInDB(userData['UserID'], userData['Message'])
        print(result)
    except Exception as ex:
        print(f"Ошибка при сохранении информации: {ex}")


@servApp.post("/getData")
async def decode(request: Request):
    encryptedData = await request.json()
    try:
        print(encryptedData)
        userData = decrypt_data(encryptedData, privateKey)
        print(userData)
        # messageUserData=userData
        if isinstance(userData, bytes):
            userData = userData.decode('utf-8')
            userData = json.loads(userData)
        print(f"Расшифрованные данные: {userData}")
        await saveInfoInDB(userData)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://127.0.0.1:{portS3}/proxy/", json=json.dumps(userData['Message']))
            print(f"Ответ от proxy: {response.status_code}, {response.text}")
        return "Отправлено"
    except Exception as e:
        print(f"Ошибка в decode: {e}")  # Вывод ошибки
        return {"status": "error", "message": str(e)}


@servApp.post("/proxy/")
async def proxy(request: Request):
    data = await request.json()
    data = json.loads(data)
    data = Masking().maskData(data)
    print(data)
    async with httpx.AsyncClient(verify=consts.cert_path) as client:
        response = await client.post(f"https://127.0.0.1:{portC1}/userPingTest", json=json.dumps(data))
        print(f"Ответ от userPingTest: {response.status_code}, {response.text}")
    return "ok"


def decrypt_data(encrypted_data: dict, private_key: rsa.PrivateKey):
    try:
        encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        nonce = base64.b64decode(encrypted_data['nonce'])
        tag = base64.b64decode(encrypted_data['tag'])
        aes_key = rsa.decrypt(encrypted_key, private_key)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return json.loads(data.decode('utf-8'))
    except (ValueError, KeyError) as e:
        raise


if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    uvicorn.run("reverseServer3:servApp", host="127.0.0.1", port=portS3, reload=True, lifespan="on")
