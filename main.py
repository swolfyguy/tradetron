from typing import Optional
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import json
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_value_byaction(action: str, value: int = 1):
    if action == "buy" or action == "long":
        return abs(value)
    elif action == "sell" or action == "short":
        return int(-abs(value))


class stock_body(BaseModel):
    stock_name: str
    action: str
    value: int
    baseurl: str
    auth_key: str


@app.post("/trade_tron")
def post_tradetron(stock_body: stock_body
                   ):
    data = {
        "auth-token": stock_body.auth_key,
        "key": stock_body.stock_name,
        "value": get_value_byaction(stock_body.action.lower(), stock_body.value)
    }
    try:
        x = requests.request(method='POST', url=stock_body.baseurl, data=data)
    except Exception as e:
        return str(e)
    return {"response": x.text, "tradetron_request": {"url": stock_body.baseurl, "data": data}}
