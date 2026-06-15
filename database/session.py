from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "advancepass.db"))
db_path = db_path.replace('\\', '/')
DATABASE_URL = f"sqlite:///{db_path}"

# Ensure data directory exists
os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
