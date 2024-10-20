import httpx
import json
import rsa

'''
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

if __name__ == "__main__":
    publicKey = getPublicKey()

    if publicKey:
        userData = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        sendData(publicKey, userData)'''
