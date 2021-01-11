import random
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Web3Library_web import W3Library
from datetime import datetime
import pandas as pd

app = FastAPI()
instance = W3Library(log_level=40)  # equals logging level error
if not instance.web3:
    raise ConnectionError("Could not connect to rpc Server")

# app.mount("/front", StaticFiles(directory="Front/public", html=True), name="front")
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO Add more type definitions for docs


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


# @app.get('/')
# async def front():
#    return RedirectResponse(url='build')
@app.get("/getAccounts")
async def getAccounts():

    return instance.accounts


@app.get("/inCharging")
async def inCharging():

    listy = instance.inCharging()
    # json = JSON.dumps(dicty)
    return listy


@app.get("/balance/{userId}")
async def getBalance(userId: str):
    try:
        balance = instance.getBalanceForUser(userId)
        return {"balance": balance * 1e-18}
    except IndexError:
        raise HTTPException(status_code=404, detail="UserId not known")


@app.get("/createAccount/{userId}")
async def newAccount(userId: str):

    if userId in instance.accounts:
        raise HTTPException(status_code=400, detail="UserId already in use. Choose another one.")

    address = instance.newAccount(userId,)
    return {"address": address}


@app.get("/startCharging/{userId}/{chargerId}/{estimatedDuration}/{desiredkWh}/{flex}")
async def startCharging(
    userId: str, chargerId: str, estimatedDuration: int, desiredkWh: float, flex: float
):
    startTime = pd.Timestamp.today()  # TODO dont use pd
    estimatedDuration = pd.Timedelta(estimatedDuration)
    print("here")
    flex, transactionHash = instance.startCharging(
        userId=userId,
        chargerId=chargerId,
        startTime=startTime,
        estimateDuration=estimatedDuration,
        desiredkWh=desiredkWh,
        flex=int(flex * 1e18),
    )
    print("there")
    if flex is None:
        raise HTTPException(status_code=400, detail="Charger already in use. Probably")
    return {
        "used_flex": flex * 1e-18,
        "transaction_hash": transactionHash,
        "startTime": startTime,
    }


@app.get("/stopCharging/{userId}/{chargerId}/{flexFlow}/{chargedkWh}")
async def stopCharging(userId: str, chargerId: str, flexFlow: float, chargedkWh: float):
    endTime = pd.Timestamp.today()

    transactionHash = instance.stopCharging(
        userId, chargerId, endTime, flexFlow, chargedkWh
    )
    return {"transaction_hash": transactionHash}


@app.get("/rand")
async def rand():
    return random.randint(0, 100)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")

if __name__ == "__main__":
    uvicorn.run("webapi:app", host="0.0.0.0", reload=True, port=8000)
