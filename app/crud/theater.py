# app/crud/theater.py
from sqlalchemy.orm import Session
from app.models.database import Theater, TheaterHall, Seat
from app.schemas.theater import TheaterCreate, TheaterHallCreate
from typing import List
import json

def create_theater(db: Session, theater: TheaterCreate):
    db_theater = Theater(**theater.dict())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

def get_theater(db: Session, theater_id: int):
    return db.query(Theater).filter(Theater.id == theater_id).first()

def get_theaters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Theater).offset(skip).limit(limit).all()

def create_theater_hall(db: Session, hall: TheaterHallCreate):
    # Create the hall
    db_hall = TheaterHall(
        theater_id=hall.theater_id,
        name=hall.name,
        total_seats=0  # Will calculate below
    )
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    
    # Create seats based on layout
    total_seats = 0
    for row_layout in hall.layout:
        row_number = row_layout.row_number
        total_seats_in_row = row_layout.total_seats
        
        # Ensure at least 6 seats per row (Algo Bharat requirement)
        if total_seats_in_row < 6:
            total_seats_in_row = 6
            
        total_seats += total_seats_in_row
        
        # Create seats for this row
        for seat_number in range(1, total_seats_in_row + 1):
            seat = Seat(
                hall_id=db_hall.id,
                row_number=row_number,
                seat_number=seat_number,
                seat_type="regular"  # Default seat type
            )
            db.add(seat)
    
    # Update total seats count
    db_hall.total_seats = total_seats
    db.commit()
    db.refresh(db_hall)
    
    return db_hall

def get_theater_halls(db: Session, theater_id: int):
    return db.query(TheaterHall).filter(TheaterHall.theater_id == theater_id).all()

def get_hall_layout(db: Session, hall_id: int):
    hall = db.query(TheaterHall).filter(TheaterHall.id == hall_id).first()
    if not hall:
        return None
    
    seats = db.query(Seat).filter(Seat.hall_id == hall_id).order_by(Seat.row_number, Seat.seat_number).all()
    
    # Group seats by row
    layout = {}
    for seat in seats:
        if seat.row_number not in layout:
            layout[seat.row_number] = []
        layout[seat.row_number].append({
            "seat_number": seat.seat_number,
            "seat_type": seat.seat_type,
            "id": seat.id
        })
    
    return {
        "hall_id": hall_id,
        "hall_name": hall.name,
        "total_seats": hall.total_seats,
        "layout": layout
    }