import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
import rsa
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
import httpx
import json
import uvicorn
import time
from maskMethods import Masking

from db import initialize_pool

servApp = FastAPI()


async def startDb():
    await initialize_pool()


(publicKey, privateKey) = rsa.newkeys(2048)

@servApp.get("/getPublicKey")
async def get_public_key():
    publicKeyUnmade = publicKey.save_pkcs1(format='PEM')
    return {"public_key": publicKeyUnmade.decode('utf-8')}

@servApp.post("/getData")
async def decode(request: Request):
    encryptedData = await request.body()
    try:
        decryptedData = rsa.decrypt(encryptedData, privateKey)
        userData = json.loads(decryptedData.decode())
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:5010/proxy/", json=userData)
            print(f"Ответ от proxy: {response.status_code}, {response.text}")
        return "Отправлено"
    except Exception as e:
        return {"status": "error", "message": str(e)}

@servApp.post("/proxy/")
async def proxy(request: Request):
    data= await request.json()
    data=data["message"]
    print(data)
    data = Masking().maskData(data)
    print(data)
    async with httpx.AsyncClient(verify='SSL/cert.pem') as client:
        response = await client.post("https://127.0.0.1:5000/userPingTest", data=json.dumps(data))
    return "ok"


if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(startDb())
    uvicorn.run("reverseServer2:servApp", host="127.0.0.1", port=5010, reload=True)


