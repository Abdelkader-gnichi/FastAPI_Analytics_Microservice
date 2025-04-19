from fastapi import APIRouter, Depends
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema, 
    EventUpdateSchema
)


from api.db.session import get_session
from sqlmodel import Session, select

router = APIRouter()

@router.get("/")
def read_events(session: Session = Depends(get_session)) -> EventListSchema:
    
    query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    results = session.exec(query).all()

    return {
        'results': results,
        'count': len(results)
    }


@router.get("/{event_id}", response_model=EventModel)
def get_event_by_id(event_id: int): # or use -> EventModel:
    return {'id': event_id}


@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema,
    session: Session = Depends(get_session)
):
    print(payload)
    data = payload.model_dump() # payload to dict

    obj = EventModel.model_validate(data)

    session.add(obj)
    session.commit()
    session.refresh(obj) # refresh the obj to get the id from db 

    return obj

@router.put("/{event_id}/")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    print(payload.description.capitalize())
    data = payload.model_dump()
    return {'id': event_id, **data}