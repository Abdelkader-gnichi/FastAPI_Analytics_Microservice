from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid


class TimestampMixin(SQLModel, table=False):
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc), nullable=False) 
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc), nullable=False)


class UUIDBase(SQLModel, table=False):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class BaseModel(UUIDBase, TimestampMixin, table=False):
    pass