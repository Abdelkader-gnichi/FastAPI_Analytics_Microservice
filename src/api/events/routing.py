from fastapi import APIRouter
from .schemas import EventSchema

router = APIRouter()

@router.get("/")
def read_events():
    return {'items': [1,2,3]}


@router.get("/{event_id}", response_model=EventSchema)
def get_event_by_id(event_id: int): # or use -> EventSchema:
    return {'id': event_id}