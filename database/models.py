from sqlalchemy import Column, Integer, String, Float, DateTime
from database.session import Base
from datetime import datetime

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String, index=True)
    strength = Column(String)
    entropy = Column(Float)
    crack_time = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ChatThread(Base):
    __tablename__ = "chat_threads"

    id = Column(String, primary_key=True, index=True) # UUID string
    title = Column(String)
    messages_json = Column(String) # Storing list of dicts as JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)
