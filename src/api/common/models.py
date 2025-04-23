import sqlmodel
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

class TimestampMixin(SQLModel, table=False):
    # created_at: datetime = Field(default_factory=get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False)
    updated_at: datetime = Field(default_factory=get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False)


class UUIDBase(SQLModel, table=False):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class BaseModel(UUIDBase, TimestampMixin, table=False):
    pass
