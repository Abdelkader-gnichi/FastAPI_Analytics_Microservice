from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema

router = APIRouter()

@router.get("/")
def read_events() -> EventListSchema:
    return {
        'results': [
            {'id':1}, {'id':2}, {'id':3}
        ],
        'count': 3
    }


@router.get("/{event_id}", response_model=EventSchema)
def get_event_by_id(event_id: int): # or use -> EventSchema:
    return {'id': event_id}


@router.post("/")
def create_event(data: dict={}) -> EventSchema:
    print(data)
    return data

@router.put("/{event_id}/")
def update_event(event_id: int, payload: dict={}):
    print(payload)
    return payload