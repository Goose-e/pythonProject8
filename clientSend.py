import asyncio
import httpx
import json
from consts import routers

# Индекс для отслеживания текущего URL
current_router = 0


# Асинхронная функция для декодирования и отправки данных
async def decode(data, url: str):
    try:
        print(data)
        encrypted_data = json.loads(data)
        print(encrypted_data['Message'])  # Вывод сообщения
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON"}

    async with httpx.AsyncClient() as client:
        # Попробуем получить публичный ключ
        try:
            dictR = await client.get(f"{url}/getPublicKey")
            if dictR.status_code == 200:
                # Декодируем ответ сервера
                publicKey = dictR.json().get('public_key')
                currentServer = dictR.json().get('server')

                if publicKey:
                    print(f"Публичный ключ успешно получен с {currentServer}")
                    # Отправляем данные на сервер
                    response = await client.post(f"{url}/sendData", json=encrypted_data)
                    return response
                else:
                    return {"status": "error", "message": "Public key not available in the response"}
            else:
                return {"status": "error", f"message": "Error fetching public key, status: {dictR.status_code}"}
        except Exception as e:
            return {"status": "error", "message": f"Exception during request: {str(e)}"}


# Асинхронная функция для обработки файла
async def func():
    global current_router
    while True:
        with open("jsonData/data.log", "r", encoding="utf-8") as file:
            for line in file:
                url = routers[current_router]  # Получаем текущий URL
                data = line.strip()  # Получаем данные
                try:
                    response = await decode(data, url)  # Передаём словарь в функцию decode
                except json.JSONDecodeError as e:
                    print(f"Ошибка декодирования JSON: {e}")
                print(f"Отправлено: {data}, Ответ: {response}")
                # Обновляем индекс для следующего URL


if __name__ == "__main__":
    asyncio.run(func())
