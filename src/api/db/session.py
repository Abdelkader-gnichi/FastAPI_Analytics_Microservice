import sqlmodel
from sqlmodel import SQLModel, Session
from .configs import DATA_BASE_URL
import time
from sqlalchemy.exc import OperationalError

if DATA_BASE_URL == "":
    raise NotImplementedError("DATA_BASE_URL variable not implemented.")

engine = sqlmodel.create_engine(DATA_BASE_URL)



def init_db(max_retries: int = 10, delay: int = 3):
    for attempt in range(max_retries):
        try:
            SQLModel.metadata.create_all(engine)
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


