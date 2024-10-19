import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
import httpx
import json
import uvicorn
import time

from db import initialize_pool

servApp = FastAPI()


async def startDb():
    await initialize_pool()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(startDb())
    uvicorn.run("reverseServer:servApp", host="127.0.0.1", port=5001, reload=True)


@servApp.post("/proxy/")
async def proxy(request: Request):
    data = await request.json()
    if "name" and "email" and "age" in list(data.keys()):
        async with httpx.AsyncClient(verify='SSL/cert.pem') as client:
            response = await client.post("https://127.0.0.1:5000/userPingTest", json=data)
        return "ok"
    else:
        print("данный метод пока не разработан")


client = TestClient(servApp)

'''
def ping():
    while True:
        time.sleep(5)
        try:
            response=client.post("/proxy/", json={"ping":"ping"})
        except:
            print("ping 0")
            continue
        else:
            print("ping 1")
            break

def test_proxy():
    response = client.post("/proxy/", json={'go':'52'})
    assert response.status_code == 200
    print(response)

while True:
    ping()
    #time.sleep(5)
    '''
