from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema, 
    EventUpdateSchema
)


from api.db.session import get_session
from sqlmodel import Session, select, delete
from uuid import UUID

router = APIRouter()

@router.get("/")
def read_events(session: Session = Depends(get_session)) -> EventListSchema:
    
    query = select(EventModel).order_by(EventModel.time.desc()).limit(10)
    results = session.exec(query).all()

    return {
        'results': results,
        'count': len(results)
    }


@router.get("/{event_id}/", response_model=EventModel)
def get_event_by_id(event_id: UUID, session: Session= Depends(get_session)): # or use -> EventModel:
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Event with id: {event_id} not found.")
    print(result, type(result))
    return result


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

@router.put("/{event_id}/", response_model=EventModel)
def update_event(event_id: UUID, payload: EventUpdateSchema, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    
    obj = session.exec(query).first()
    print('result', obj)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id: {event_id} doesn't exists.")
    
    # only update given fields and leave other with thier original values 
    update_data = payload.model_dump(exclude_unset=True)
    
    for k, v in update_data.items():
        setattr(obj, k, v)
    
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{event_id}/")
def delete_event_by_id(event_id: UUID, session: Session = Depends(get_session)):
    query = delete(EventModel).where(EventModel.id == event_id)
    result = session.exec(query)

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"event with id: {event_id} not found.")
    
    session.commit()

        # or Response(status_code=status.HTTP_204_NO_CONTENT) without a body
    return JSONResponse({'detail': 'record deleted successfully.'}, status_code=status.HTTP_200_OK)