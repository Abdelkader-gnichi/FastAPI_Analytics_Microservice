from fastapi import APIRouter
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema, 
    EventUpdateSchema
)
import os
from api.db.configs import DATA_BASE_URL

router = APIRouter()

@router.get("/")
def read_events() -> EventListSchema:
    print(os.environ.get('DATA_BASE_URL'), '|', DATA_BASE_URL)
    return {
        'results': [
            {'id':1}, {'id':2}, {'id':3}
        ],
        'count': 3
    }


@router.get("/{event_id}", response_model=EventModel)
def get_event_by_id(event_id: int): # or use -> EventModel:
    return {'id': event_id}


@router.post("/")
def create_event(payload: EventCreateSchema) -> EventModel:
    print(payload)
    data = payload.model_dump()
    return {'id' : 1, **data}

@router.put("/{event_id}/")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    print(payload.description.capitalize())
    data = payload.model_dump()
    return {'id': event_id, **data}