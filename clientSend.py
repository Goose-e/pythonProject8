import time
import httpx
import json
import rsa
from consts import routers

current_router = 0

while True:
    with open("jsonData/data.log", "r", encoding="utf-8") as file:
        for line in file:
            url = routers[current_router]
            data = json.loads(line)
            response = httpx.post(f"{url}/getData", json=data)
            print(f"Отправлено: {data}, Ответ: {response.status_code}")
            current_router = (current_router + 1) % len(routers)
