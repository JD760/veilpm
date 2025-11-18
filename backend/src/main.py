from typing import Union
import os

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"env": os.getenv("BACKEND_PORT")}
    #return {"Hello": "Docker"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None) -> dict[str, int | str | None]:
    return {"item_id": item_id, "q": q}