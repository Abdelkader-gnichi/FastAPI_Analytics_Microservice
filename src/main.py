from typing import Union

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def greeting():
    return {'hello': 'worlder'}

@app.get('/items/{item_id}/')
def get_item_by_id(item_id: int, q: Union[str, None] = None):
    return {'item_id:': item_id, 'q': q}


@app.get("/healthz")
def get_health_status():
    return {'status': 'ok'}