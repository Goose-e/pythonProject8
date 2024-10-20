import time

import httpx
import json
import rsa

url = "http://127.0.0.1:5020/getData"

while True:
    with open("jsonData/data.log", "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            response = httpx.post(url, json=data)
            print(f"Отправлено: {data}, Ответ: {response.status_code}")