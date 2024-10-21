import base64
import json
import logging

import rsa
import httpx
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

from consts import portR2, servers, portS1
from routers.metrics import REQUEST_COUNT, REQUEST_LATENCY

router2 = FastAPI()

current_server = 0
server = None


@router2.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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


cached_public_key = None


@router2.get("/getPublicKey")
async def getPublicKey():
    async with httpx.AsyncClient() as client:
        print("зашло")
        response = await client.get(f"{servers[current_server]}/getPublicKeyServer")
        return response.json()


@router2.post("/sendData")
async def sendData(request:Request):
    data = await request.json()
    print(type(data))
    next_server = get_next_server()
    print(next_server)
    url = f"{next_server}/getData"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            print("Ok")
        else:
            print(f"Ошибка отправки данных: {response.status_code}")


if __name__ == '__main__':
    uvicorn.run(router2, host="0.0.0.0", port=portR2)
