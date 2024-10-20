from fastapi import FastAPI, HTTPException
import requests
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

@router1.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

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