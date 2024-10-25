import asyncio
import base64
from asyncio import WindowsSelectorEventLoopPolicy
from datetime import datetime

import rsa
from fastapi import FastAPI, Request
from Cryptodome.Cipher import AES
import httpx
import json
import uvicorn

import consts
import db
from consts import portS2, portC1
from maskMethods import Masking
from db import DaBa
from models.FullUser import FullUser
from models.UserInfo import UserInfo
from servers.IServer import IServer

servApp = FastAPI()
dataBase: DaBa


class MyServer(IServer):

    async def getRegulars(self):
        regulars = await getRegulars()
        return regulars


serverInstance = MyServer()


async def getRegulars():
    try:
        dataBase = db.DaBa1()
        print(type(dataBase.con))
        result = await dataBase.getAllRegulars()
        return result
    except Exception as ex:
        print(f"Ошибка при получения информации: {ex}")


async def authAdmin(email, password):
    try:
        dataBase = db.DaBa1()
        print(type(dataBase.con))
        result = await dataBase.getAdminFromDB(email, password)
        return result
    except Exception as ex:
        print(f"Ошибка при получении информации: {ex}")
        return None



async def lifespan(scope, receive, send):
    if scope['type'] == 'lifespan':
        global dataBase
        dataBase = DaBa()
        await db.initialize_pool()
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


@servApp.get("/getPublicKeyServer")
async def get_public_key():
    try:
        publicKeyUnmade = publicKey.save_pkcs1(format='PEM')  # Преобразуем публичный ключ в формат PEM
        return {"public_key": publicKeyUnmade.decode('utf-8')}  # Возвращаем строковое представление ключа
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def saveInfoInDB(data, Message, flag):
    try:
        print(data, Message, flag)
        if not flag:
            userInfo = UserInfo(
                userInfoId=0,
                userId=data['UserID'],
                secretInfo=Message,
                endpoint=data['Endpoint'],
                timestamp=data['Timestamp']
            )
            result = await dataBase.saveInfoInDB(userInfo)
            print(result)
        else:
            print("не чд")
    except Exception as ex:
        print(f"Ошибка при сохранении информации: {ex}")


@servApp.post("/getData")
async def decode(request: Request):
    encryptedData = await request.json()
    encryptedData = json.loads(encryptedData)
    try:
        print(encryptedData)
        userData = decrypt_data(encryptedData, privateKey)
        print(userData)
        # messageUserData=userData
        if isinstance(userData, bytes):
            userData = userData.decode('utf-8')
            userData = json.loads(userData)
        print(f"Расшифрованные данные: {userData}")
        user = await dataBase.findUserByUserId(userData['UserID'])
        birthdate_str = userData.get('Дата рождения')
        # ↓☠️☠️
        if birthdate_str:
            birthdate = datetime.strptime(birthdate_str, '%d.%m.%Y').date()
        else:
            birthdate = None  # Или можно установить другое значение по умолчанию
        if user is None:
            user = FullUser(
                user_id=userData['UserID'],
                email=userData['Email'],
                login=userData['Login'],
                support_level=userData['SupportLevel'],
                age=userData.get('Возраст'),
                birthdate=birthdate,
                first_name=userData.get('Имя'),
                second_name=userData.get('Фамилия'),
                last_name=userData.get('Отчество'),
                gender=userData.get('Пол'),
                phone_number=userData.get('Номер телефона')
            )
            await dataBase.saveFullUser(user)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://127.0.0.1:{portS2}/proxy/", json=userData)
            print(f"Ответ от proxy: {response.status_code}, {response.text}")
        return "Отправлено"
    except Exception as e:
        print(f"Ошибка в decode: {e}")  # Вывод ошибки
        return {"status": "error", "message": str(e)}


@servApp.post("/proxy/")
async def proxy(request: Request):
    # await MaskControl.changeMaskType(2)
    maskType = await MaskControl().takeMask()
    data = await request.json()
    print(type(data))
    try:
        cheat = data[1]
        data = data[0]
        await MaskControl.changeMaskType(cheat)
        return "ok"
    except:
        data['Message'], flag, text = await Masking().maskData(data['Message'], int(maskType), serverInstance)
    await saveInfoInDB(data, text, flag)
    print(data)
    if flag is not False:
        async with httpx.AsyncClient(verify=consts.cert_path) as client:
            response = await client.post(f"https://127.0.0.1:{portC1}/userPingTest", json=json.dumps(data['Message']))
            print(f"Ответ от userPingTest: {response.status_code}, {response.text}")
    return "ok"


def decrypt_data(encrypted_data: dict, private_key: rsa.PrivateKey):
    try:
        encrypted_key = base64.b64decode(encrypted_data["encrypted_key"])
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        nonce = base64.b64decode(encrypted_data["nonce"])
        tag = base64.b64decode(encrypted_data["tag"])
        aes_key = rsa.decrypt(encrypted_key, private_key)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return json.loads(data.decode('utf-8'))
    except (ValueError, KeyError) as e:
        raise


class MaskControl():
    @staticmethod
    async def changeMaskType(Stype):
        file = open("serverMask.txt", "w", encoding="utf-8")
        file.write(str(Stype))
        file.close()
        (print("ffffffffffffffffffffffff"))

    @staticmethod
    async def takeMask(cheatLoL=0):
        if cheatLoL == 0:
            file = open("serverMask.txt", "r", encoding="utf-8")
            maskType = file.readline().replace("\n", "")
            print(f"Mask={maskType}")
            file.close()
            return maskType
        else:
            file = open("serverMask.txt", "w", encoding="utf-8")
            file.write(str(cheatLoL))
            file.close()
            print("ffffffffffffffffffffffff")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    uvicorn.run("reverseServer1:servApp", host="127.0.0.1", port=portS2, reload=True, lifespan="on")
