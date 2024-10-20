from fastapi import FastAPI, HTTPException
import requests
import httpx
import rsa
import json
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

router1 = FastAPI

REQUEST_COUNT = Counter('balance_request_count', 'Количество запросов, обработанных балансировщиком')
REQUEST_LATENCY = Histogram('balance_request_latency_seconds', 'Задержка обработки запросов балансировщиком')

servers = [
    'http://localhost:'
    'http://localhost:'
    'http://localhost:'
]

def getPublicKey():
    response = httpx.get("http://127.0.0.1:5001/getPublicKey")
    if response.status_code == 200:
        publicKeyUnmade = response.json()["public_key"]
        publicKey = rsa.PublicKey.load_pkcs1(publicKeyUnmade.encode('utf-8'))
        return publicKey
    else:
        print(f"Ошибка получения публичного ключа: {response.status_code}")
        return None

def sendData(public_key, data):
    encrypted_data = rsa.encrypt(json.dumps(data).encode(), public_key)
    url = "http://127.0.0.1:5001/getData"
    response = httpx.post(url, content=encrypted_data)
    if response.status_code == 200:
        print("Ok")
    else:
        print(f"Ошибка отправки данных: {response.status_code}")


@router1.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def get_next_server():
    global current_server
    server = servers[current_server]
    current_server = (current_server + 1) % len(servers)
    return server


@router1.post("/send")
async def balance_request(data: dict):
    next_server = get_next_server()  # Выбираем следующий сервер
    REQUEST_COUNT.inc()  # Увеличиваем счётчик запросов
    start_time = time.time()  # Время начала запроса для измерения задержки

    try:
        # Отправляем данные на выбранный сервер
        response = requests.post(f"{next_server}/process", json=data)
        REQUEST_LATENCY.observe(time.time() - start_time)  # Измеряем задержку и записываем её
        return response.json()  # Возвращаем ответ от сервера клиенту
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(router1, host="0.0.0.0", port=8000)
    publicKey = getPublicKey()

    if publicKey:
        userData = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        sendData(publicKey, userData)
