import json
import Cryptodome.Cipher
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

from consts import portR1
from metrics import REQUEST_COUNT, REQUEST_LATENCY

router1 = FastAPI()

servers = [
    'http://localhost:8000',
    'http://localhost:8001',
    'http://localhost:8002'
]

current_server = 0


@router1.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def encrypt_data(data, public_key):
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(json.dumps(data).encode())

    encrypted_key = rsa.encrypt(aes_key, public_key)

    return {
        'encrypted_key': encrypted_key,
        'ciphertext': ciphertext,
        'nonce': cipher_aes.nonce,
        'tag': tag
    }


def get_next_server():
    global current_server
    server = servers[current_server]
    current_server = (current_server + 1) % len(servers)
    return server


@router1.post("/send")
async def balance_request(data: dict):
    next_server = get_next_server()
    REQUEST_COUNT.inc()
    start_time = time.time()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{next_server}/process", json=data)
            REQUEST_LATENCY.observe(time.time() - start_time)
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router1.get("/getPublicKey")
async def getPublicKey():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:5010/getPublicKey")
        if response.status_code == 200:
            publicKeyUnmade = response.json()["public_key"]
            publicKey = rsa.PublicKey.load_pkcs1(publicKeyUnmade.encode('utf-8'))
            return publicKey
        else:
            print(f"Ошибка получения публичного ключа: {response.status_code}")
            return None


@router1.post("/sendData")
async def sendData(public_key, data):
    encrypted_data = encrypt_data(data, public_key)
    url = "http://127.0.0.1:5010/getData"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=encrypted_data)
        if response.status_code == 200:
            print("Ok")
        else:
            print(f"Ошибка отправки данных: {response.status_code}")


@router1.post("/getData")
async def decode(request: Request):
    data = await request.body()
    try:
        encrypted_data = json.loads(data.decode())
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON"}
    publicKey = await getPublicKey()
    if publicKey is not None:
        response = await sendData(publicKey, encrypted_data)
        return response
    else:
        return {"status": "error", "message": "Public key not available"}


if __name__ == '__main__':
    uvicorn.run(router1, host="0.0.0.0", port=portR1)
