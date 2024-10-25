import httpx
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from prometheus_client import generate_latest, Counter, Histogram, Summary
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

from consts import portR2, servers, portS1

REQUEST_COUNT = Counter('balance_request_count', 'Количество запросов, обработанных балансировщиком')
REQUEST_LATENCY = Histogram('balance_request_latency_seconds', 'Задержка обработки запросов балансировщиком',
                            ['endpoint'])
REQUEST_ERROR_COUNT = Counter('balance_request_error_count', 'Количество ошибок, возникших при обработке запросов')
latency_summary = Summary('latency', 'Latency of requests in seconds', ['endpoint'])

router2 = FastAPI()

current_server = 0
server = None


@router2.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


async def get_next_server():
    global current_server
    global server
    server = servers[current_server]
    current_server = (current_server + 1) % len(servers)
    return server


@router2.post("/send")
async def balance_request(request: Request):
    global current_server
    data = await request.json()
    REQUEST_COUNT.inc()
    start_time = time.time()
    next_server = servers[current_server]
    current_server = (current_server + 1) % len(servers)
    url = f"{next_server}/getData"
    try:
        with latency_summary.labels(endpoint='/getData').time():
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{url}", json=data)
                latency = time.time() - start_time
                REQUEST_LATENCY.labels(endpoint='/getData').observe(latency)
                return response.json()
    except Exception as e:
        REQUEST_ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))


cached_public_key = None


@router2.get("/getPublicKey")
async def getPublicKey():
    async with httpx.AsyncClient() as client:
        print("зашло")
        response = await client.get(f"{servers[current_server]}/getPublicKeyServer")
        return response.json()


# @router1.post("/sendData")
# async def sendData(request: Request):
#     data = await request.json()
#     print(f"Полученные данные: {data}")  # Логируем полученные данные
#     next_server = get_next_server()
#     url = f"{next_server}/getData"
#     print(f"Отправка данных на: {url}")  # Логируем URL
#
#     async with httpx.AsyncClient(timeout=10) as client:
#         try:
#             response = await client.post(url, json=data)  # Здесь важно, чтобы data был словарем
#             print(f"Ответ от {url}: {response.status_code}, {response.text}")  # Логируем ответ
#
#             if response.status_code == 200:
#                 print("Ok")
#                 return {"status": "success", "data": response.json()}
#             else:
#                 print(f"Ошибка отправки данных: {response.status_code}, Ответ: {response.text}")
#                 raise HTTPException(status_code=response.status_code, detail=response.text)
#         except httpx.RequestError as e:
#             print(f"Ошибка при отправке запроса: {e}")
#             raise HTTPException(status_code=500, detail=str(e))
#         except Exception as e:
#             print(f"Неожиданная ошибка: {e}")
#             raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(router2, host="0.0.0.0", port=portR2)
