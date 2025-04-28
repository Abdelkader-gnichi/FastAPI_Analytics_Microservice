from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status
from .models import (
    EventModel, 
    EventListSchema,
    EventBucketSchema,
    EventCreateSchema, 
    # EventUpdateSchema
)


from api.db.session import get_session
from sqlmodel import Session, select, delete
from uuid import UUID

from sqlalchemy import  func, case
from timescaledb.hyperfunctions import time_bucket
from typing import List


router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
    '/', '/about', '/pricing', '/contact', 
    '/blog', '/products', '/login', '/register',
    '/services', '/support', '/dashboard', '/settings'
]

@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default='1 day'),
    pages: List = Query(default=None),
    session: Session = Depends(get_session)
): #  -> EventListSchema
    
    # query = select(EventModel).order_by(EventModel.time.desc()).limit(10)
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    os_case = case(
        (EventModel.user_agent.ilike('%Windows%'), 'Windows'),
        (EventModel.user_agent.ilike('%macintosh%'), 'MacOS'),
        (EventModel.user_agent.ilike('%iphone%'), 'IOS'),
        (EventModel.user_agent.ilike('%android%'), 'Android'),
        (EventModel.user_agent.ilike('%linux%'), 'Linux'),
        else_='Other'
    ).label('operating_system')
    
    query = select(
        bucket.label('bucket'),
        EventModel.page.label('page'),
        # EventModel.user_agent.label('ua'),
        os_case,
        func.avg(EventModel.duration).label('avg_duration'),
        func.count().label('count')
    ).where(
        EventModel.page.in_(lookup_pages)
    ).group_by(
        bucket,
        EventModel.page,
        # EventModel.user_agent
        os_case
    ).order_by(
        bucket,
        EventModel.page,
        # EventModel.user_agent
        os_case
    )
    results = session.exec(query).all()

    return results


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

# @router.put("/{event_id}/", response_model=EventModel)
# def update_event(event_id: UUID, payload: EventUpdateSchema, session: Session = Depends(get_session)):
#     query = select(EventModel).where(EventModel.id == event_id)
    
#     obj = session.exec(query).first()
#     print('result', obj)
#     if not obj:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id: {event_id} doesn't exists.")
    
#     # only update given fields and leave other with thier original values 
#     update_data = payload.model_dump(exclude_unset=True)
    
#     for k, v in update_data.items():
#         setattr(obj, k, v)
    
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj

@router.delete("/{event_id}/")
def delete_event_by_id(event_id: UUID, session: Session = Depends(get_session)):
    query = delete(EventModel).where(EventModel.id == event_id)
    result = session.exec(query)

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"event with id: {event_id} not found.")
    
    session.commit()

        # or Response(status_code=status.HTTP_204_NO_CONTENT) without a body
    return JSONResponse({'detail': 'record deleted successfully.'}, status_code=status.HTTP_200_OK)