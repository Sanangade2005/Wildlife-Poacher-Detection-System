from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime
)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

import os

# ---------------------------------
# PostgreSQL configuration (can be overridden by environment variable)
# ---------------------------------
DATABASE_URL = "postgresql+psycopg2://postgres:bala1234@127.0.0.1:5432/poacher_db"
print(f"DEBUG: Connecting to database at {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------------------------
# User Table
# ---------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    ranger_id = Column(String, nullable=False, unique=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    email_or_phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------
# Video Detection Table
# ---------------------------------
class VideoDetection(Base):
    __tablename__ = "video_detections"

    id = Column(Integer, primary_key=True)

    ranger_id = Column(String, nullable=False)
    frame_path = Column(String, nullable=False)

    yolo_detected = Column(Boolean, default=False)
    gemini_detected = Column(Boolean, default=False)

    gemini_confidence = Column(Float)
    gemini_reason = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------
# Photo Detection Table
# ---------------------------------
class PhotoDetection(Base):
    __tablename__ = "photo_detections"

    id = Column(Integer, primary_key=True)

    ranger_id = Column(String, nullable=False)
    image_path = Column(String, nullable=False)

    yolo_detected = Column(Boolean, default=False)
    gemini_detected = Column(Boolean, default=False)

    gemini_confidence = Column(Float)
    gemini_reason = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------
# Create tables
# ---------------------------------
def init_db():
    Base.metadata.create_all(bind=engine)
