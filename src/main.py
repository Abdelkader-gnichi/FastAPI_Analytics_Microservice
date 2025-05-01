from contextlib import asynccontextmanager
from typing import Union
from api.db.session import init_db
from fastapi import FastAPI
from api.events import router as events_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before startup
    init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

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
