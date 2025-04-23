import sqlmodel
from sqlmodel import SQLModel, Session
from .configs import DATABASE_URL, DB_TIMEZONE
import time
from sqlalchemy.exc import OperationalError
import timescaledb

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL variable not implemented.")
    
# use sqlmodel for tradition pg models, but here we are using timescale once
engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)



def init_db(max_retries: int = 10, delay: int = 3):
    for attempt in range(max_retries):
        try:
            # to create tradition pg tables
            SQLModel.metadata.create_all(engine)
            # to create time series (timescale) tables
            timescaledb.metadata.create_all(engine)
            print("✅ DB initialized")
            return
        except OperationalError as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print("💥 All DB connection attempts failed.")
                raise



def get_session():
    with Session(engine) as session:
        yield session
