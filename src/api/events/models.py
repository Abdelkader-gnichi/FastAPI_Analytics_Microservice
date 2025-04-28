from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field
from api.common.models import BaseModel
from timescaledb import TimescaleModel

class EventModel(BaseModel, TimescaleModel, table=True):
    page: str = Field(index=True)
    ip_address: Optional[str] = Field(default='', index=True)
    user_agent: Optional[str] = Field(default='', index=True)
    referrer: Optional[str] = Field(default='', index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)
    description: Optional[str] = Field(default="Default DEsc")

    _chunk_time_interval__= "INTERVAL 1 day"
    __drop_after__= "INTERVAL 3 months"



class EventListSchema(SQLModel):

    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):
    page: str = Field(index=True)
    ip_address: Optional[str] = Field(default='', index=True)
    user_agent: Optional[str] = Field(default='', index=True)
    referrer: Optional[str] = Field(default='', index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)
    description: Optional[str] = Field(default="Default DEsc")


# class EventUpdateSchema(SQLModel):
#     page: Optional[str] = None
#     description: Optional[str] = None


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int
