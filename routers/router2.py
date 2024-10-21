import base64
import json
import logging

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import rsa
import httpx
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

from consts import servers, portS1, portR2
from routers.metrics import REQUEST_COUNT, REQUEST_LATENCY

router2 = FastAPI()

current_server = 0
server = None


@router2.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def encrypt_data(data, public_key):
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(json.dumps(data).encode())

    encrypted_key = rsa.encrypt(aes_key, public_key)

    # Кодируем значения в base64
    return {
        'encrypted_key': base64.b64encode(encrypted_key).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'nonce': base64.b64encode(cipher_aes.nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }


def get_next_server():
    global current_server
    global server
    server = servers[current_server]
    current_server = (current_server + 1) % len(servers)
    return server


@router2.post("/send")
async def balance_request(data: dict):
    REQUEST_COUNT.inc()
    start_time = time.time()
    try:
        async with httpx.AsyncClient() as client:
            print(server)
            response = await client.post(f"{server}/process", json=data)
            REQUEST_LATENCY.observe(time.time() - start_time)
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router2.get("/getPublicKey")
async def getPublicKey():
    try:
        # Используем асинхронный HTTP-клиент для получения ключа
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{servers[current_server]}/getPublicKey")

            # Если ответ успешен, извлекаем публичный ключ
            if response.status_code == 200:
                publicKeyUnmade = response.json().get("public_key")

                if publicKeyUnmade:
                    # Декодируем ключ
                    publicKey = rsa.PublicKey.load_pkcs1(publicKeyUnmade.encode('utf-8'))
                    return {"public_key": publicKey, "server": servers[current_server]}
                else:
                    return {"status": "error", "message": "Ключ отсутствует в ответе"}
            else:
                return {"status": "error", "message": f"Ошибка получения публичного ключа: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(f"{server[current_server]}/getPublicKey")
    #     if response.status_code == 200:
    #         publicKeyUnmade = response.json()["public_key"]
    #         publicKey = rsa.PublicKey.load_pkcs1(publicKeyUnmade.encode('utf-8'))
    #         cached_public_key = publicKey  # Обновляем время кэширования
    #         return publicKey
    #     else:
    #         print(f"Ошибка получения публичного ключа: {response.status_code}")
    #         return None


@router2.post("/sendData")
async def sendData(public_key, data):
    encrypted_data = encrypt_data(data, public_key)
    next_server = get_next_server()
    print(next_server)
    url = f"{next_server}/getData"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=encrypted_data)
        if response.status_code == 200:
            print("Ok")
        else:
            print(f"Ошибка отправки данных: {response.status_code}")




if __name__ == '__main__':
    uvicorn.run(router2, host="0.0.0.0", port=portR2)
