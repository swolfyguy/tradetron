from typing import Optional
import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_value_byaction(action: str, value: int = 1):
    if action == "buy" or action == "long":
        return abs(value)
    elif action == "sell" or action == "short":
        return int(-abs(value))


@app.post("/trade_tron")
def post_tradetron(stock_name: str, action: str, value: int,
              baseurl: str = "https://api.tradetron.tech/api1.php",
              auth_key: str = "",
              ):
    data = {
        "auth-token": auth_key,
        "key": stock_name,
        "value": get_value_byaction(action.lower(), value)
    }

    x = requests.request(method='POST', url=baseurl, data=data)
    return {"response": x.text, "tradetron_request": {"url": baseurl, "data": data}}
