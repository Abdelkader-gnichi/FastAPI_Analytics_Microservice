import sqlmodel
from sqlmodel import SQLModel
from .configs import DATA_BASE_URL

if DATA_BASE_URL == "":
    raise NotImplementedError("DATA_BASE_URL variable not implemented.")

engine = sqlmodel.create_engine(DATA_BASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)