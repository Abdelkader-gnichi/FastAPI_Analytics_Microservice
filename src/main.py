from typing import Union

from fastapi import FastAPI
from api.events import router as events_router


app = FastAPI()
app.include_router(events_router, prefix='/api/events')

@app.get("/")
def greeting():
    return {'hello': 'world'}

@app.get('/items/{item_id}/')
def get_item_by_id(item_id: int, q: Union[str, None] = None):
    return {'item_id:': item_id, 'q': q}


@app.get("/healthz")
def get_api_health_status():
    return {'status': 'ok'}