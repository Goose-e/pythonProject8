import json
from ctypes import windll
import rsa
import httpx
from fastapi import FastAPI, HTTPException
import uvicorn
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from metrics import REQUEST_COUNT, REQUEST_LATENCY
from config import servers

router2 = FastAPI()



current_server = 0


@router2.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def get_next_server():
    global current_server
    server = servers[current_server]
    current_server = (current_server + 1) % len(servers)
    return server


@router2.post("/send")
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


@router2.get("/getPublicKey")
async def getPublicKey():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:5001/getPublicKey")
        if response.status_code == 200:
            publicKeyUnmade = response.json()["public_key"]
            publicKey = rsa.PublicKey.load_pkcs1(publicKeyUnmade.encode('utf-8'))
            return publicKey
        else:
            print(f"Ошибка получения публичного ключа: {response.status_code}")
            return None


@router2.post("/sendData")
async def sendData(public_key, data):
    encrypted_data = rsa.encrypt(json.dumps(data).encode(), public_key)
    url = "http://127.0.0.1:5001/getData"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=encrypted_data)
        if response.status_code == 200:
            print("Ok")
        else:
            print(f"Ошибка отправки данных: {response.status_code}")


if __name__ == '__main__':
    uvicorn.run(router2, host="0.0.0.0", port=4001)
