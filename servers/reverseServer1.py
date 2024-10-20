import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
import rsa
from fastapi import FastAPI, Request
from Cryptodome.Cipher import AES

import httpx
import json
import uvicorn
import time

import consts
from consts import portS1
from maskMethods import Masking

from db import initialize_pool

servApp = FastAPI()


async def startDb():
    await initialize_pool()


(publicKey, privateKey) = rsa.newkeys(2048)

@servApp.get("/getPublicKey")
async def get_public_key():
    publicKeyUnmade = publicKey.save_pkcs1(format='PEM')
    return {"public_key": publicKeyUnmade.decode('utf-8')}

@servApp.post("/getData")
async def decode(request: Request):
    encryptedData = await request.body()
    try:
        userData = decrypt_data(encryptedData, privateKey)

        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:5010/proxy/", json=userData)
            print(f"Ответ от proxy: {response.status_code}, {response.text}")
        return "Отправлено"
    except Exception as e:
        return {"status": "error", "message": str(e)}

@servApp.post("/proxy/")
async def proxy(request: Request):
    data= await request.json()
    data=data["message"]
    print(data)
    data = Masking().maskData(data)
    print(data)
    async with httpx.AsyncClient(verify=consts.cert_path) as client:
        response = await client.post("https://127.0.0.1:5000/userPingTest", data=json.dumps(data))
    return "ok"


def decrypt_data(encrypted_data, private_key):
    encrypted_key = encrypted_data['encrypted_key']
    ciphertext = encrypted_data['ciphertext']
    nonce = encrypted_data['nonce']
    tag = encrypted_data['tag']
    aes_key = rsa.decrypt(encrypted_key, private_key)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return json.loads(data.decode())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(startDb())
    uvicorn.run("reverseServer1:servApp", host="127.0.0.1", port=portS1, reload=True)


