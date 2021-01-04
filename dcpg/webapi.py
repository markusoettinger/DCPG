from typing import Optional
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import random

from pydantic import BaseModel

app = FastAPI()

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

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


# @app.get('/')
# async def front():
#    return RedirectResponse(url='build')

@app.get("/rand")
async def rand():
  return random.randint(0, 100)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")

if __name__ == "__main__":
    uvicorn.run("webapi:app", host="0.0.0.0", reload=True, port=8000)