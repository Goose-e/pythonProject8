import asyncio
import base64
import httpx
import json
import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from consts import routers

current_router = 0


def encrypt_data(data, public_key):
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(json.dumps(data).encode())
    encrypted_key = rsa.encrypt(aes_key, public_key)
    return {
        'encrypted_key': base64.b64encode(encrypted_key).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'nonce': base64.b64encode(cipher_aes.nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }


async def clientStart():
    global current_router
    while True:
        with open("jsonData/data.log", "r", encoding="utf-8") as file:
            for line in file:
                async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                    data = json.loads(line)
                    print(data)
                    response = await client.get(f"{routers[current_router]}/getPublicKey")
                    if response.status_code == 200:
                        publicKeyUnmade = response.json().get("public_key")
                        publicKey = rsa.PublicKey.load_pkcs1(publicKeyUnmade.encode('utf-8'))
                        url = routers[current_router]
                        current_router = (current_router + 1) % len(routers)
                        data = encrypt_data(data, publicKey)
                        response = await client.post(f"{url}/send", json=json.dumps(data))
                        print(f"Отправлено: {data}, Ответ: {response.status_code}")

                    else:
                        print("error:", response.status_code)


if __name__ == "__main__":
    asyncio.run(clientStart())
