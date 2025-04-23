from typing import List, Optional
from sqlmodel import SQLModel, Field
from api.common.models import BaseModel
from timescaledb import TimescaleModel

class EventModel(BaseModel, TimescaleModel, table=True):
    page: str = Field(index=True)
    description: Optional[str] = Field(default="Default DEsc")
    
    _chunk_time_interval__: str = "INTERVAL 1 day"
    __drop_after__:  str = "INTERVAL 3 months"
        


class EventListSchema(SQLModel):

    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = ""


class EventUpdateSchema(SQLModel):
    page: Optional[str] = None
    description: Optional[str] = None
