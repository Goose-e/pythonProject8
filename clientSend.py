import httpx
import json

def userDataPing():
    userData = {
        "name": "zxc",
        "email": "zxc@example.com",
        "age": 52
    }
    url = "http://127.0.0.1:5001/proxy/"

    try:
        response = httpx.post(url, json=userData)

        if response.status_code == 200:
            print("Ответ от сервера:", response.text)
        else:
            print(f"Статус код: {response.status_code}")

    except httpx.HTTPError as e:
        print(f"Произошла ошибка при запросе: {e}")


if __name__ == "__main__":
    userDataPing()
