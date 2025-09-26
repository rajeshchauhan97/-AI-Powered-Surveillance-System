# app/models/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Use SQLite for development
DATABASE_URL = "sqlite:///./movie_booking.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    genre = Column(String(100))
    language = Column(String(50))
    release_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shows = relationship("Show", back_populates="movie")

class Theater(Base):
    __tablename__ = "theaters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    halls = relationship("TheaterHall", back_populates="theater")

class TheaterHall(Base):
    __tablename__ = "theater_halls"
    
    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"))
    name = Column(String(100), nullable=False)
    total_seats = Column(Integer)
    layout_json = Column(Text)  # Store seat layout as JSON
    
    theater = relationship("Theater", back_populates="halls")
    shows = relationship("Show", back_populates="hall")
    seats = relationship("Seat", back_populates="hall")

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    hall_id = Column(Integer, ForeignKey("theater_halls.id"))
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(String(50), default="regular")  # regular, premium, etc.
    
    hall = relationship("TheaterHall", back_populates="seats")
    bookings = relationship("BookingSeat", back_populates="seat")

class Show(Base):
    __tablename__ = "shows"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("theater_halls.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    movie = relationship("Movie", back_populates="shows")
    hall = relationship("TheaterHall", back_populates="shows")
    bookings = relationship("Booking", back_populates="show")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    user_id = Column(Integer, default=1)  # Default user for demo
    booking_reference = Column(String(100), unique=True, index=True)
    total_amount = Column(Float)
    booking_status = Column(String(50), default="confirmed")  # confirmed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    show = relationship("Show", back_populates="bookings")
    seats = relationship("BookingSeat", back_populates="booking")

class BookingSeat(Base):
    __tablename__ = "booking_seats"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    
    booking = relationship("Booking", back_populates="seats")
    seat = relationship("Seat", back_populates="bookings")

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")