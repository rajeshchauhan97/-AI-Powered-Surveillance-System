from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL - Use SQLite for development
SQLALCHEMY_DATABASE_URL = "sqlite:///./movie_booking.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Models
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    genre = Column(String(50), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, nullable=False)
    hall_number = Column(Integer, nullable=False)
    total_rows = Column(Integer, nullable=False)
    seats_per_row = Column(JSON, nullable=False)  # Stores {"A": 8, "B": 7, ...}
    created_at = Column(DateTime, default=datetime.utcnow)

class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False)
    theater_id = Column(Integer, nullable=False)
    hall_id = Column(Integer, nullable=False)
    show_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String(50), unique=True, nullable=False)
    show_id = Column(Integer, nullable=False)
    user_ids = Column(JSON, nullable=False)  # Stores [1, 2, 3]
    seats = Column(JSON, nullable=False)     # Stores ["A1", "A2", "A3"]
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)