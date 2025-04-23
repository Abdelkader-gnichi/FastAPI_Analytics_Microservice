from typing import List, Optional
from sqlmodel import SQLModel, Field
from api.common.models import BaseModel


class EventModel(BaseModel, table=True):
    page: Optional[str] = ""
    description: Optional[str] = Field(default="Default DEsc")


class EventListSchema(SQLModel):

    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = ""


class EventUpdateSchema(SQLModel):
    page: Optional[str] = None
    description: Optional[str] = None
