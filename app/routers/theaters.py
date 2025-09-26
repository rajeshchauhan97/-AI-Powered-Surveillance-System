# app/routers/theaters.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.schemas.theater import Theater, TheaterCreate, TheaterHall, TheaterHallCreate
from app.utils.database import get_db
from app.models import Theater as TheaterModel, TheaterHall as TheaterHallModel, Seat

router = APIRouter(prefix="/theaters", tags=["theaters"])

@router.get("/", response_model=List[Theater])
def read_theaters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    theaters = db.query(TheaterModel).offset(skip).limit(limit).all()
    return theaters

@router.get("/{theater_id}", response_model=Theater)
def read_theater(theater_id: int, db: Session = Depends(get_db)):
    theater = db.query(TheaterModel).filter(TheaterModel.id == theater_id).first()
    if theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater

@router.post("/", response_model=Theater)
def create_theater(theater: TheaterCreate, db: Session = Depends(get_db)):
    db_theater = TheaterModel(**theater.model_dump())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

@router.post("/halls", response_model=TheaterHall)
def create_theater_hall(hall: TheaterHallCreate, db: Session = Depends(get_db)):
    # Calculate total seats
    total_seats = sum(row.total_seats for row in hall.layout)
    
    # Create hall
    db_hall = TheaterHallModel(
        theater_id=hall.theater_id,
        name=hall.name,
        total_seats=total_seats,
        layout_json=json.dumps([row.model_dump() for row in hall.layout])
    )
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    
    # Create seats
    for row_layout in hall.layout:
        for seat_num in range(1, row_layout.total_seats + 1):
            seat = Seat(
                hall_id=db_hall.id,
                row_number=row_layout.row_number,
                seat_number=seat_num,
                seat_type="regular"
            )
            db.add(seat)
    
    db.commit()
    
    return TheaterHall(
        id=db_hall.id,
        theater_id=db_hall.theater_id,
        name=db_hall.name,
        layout=hall.layout,
        total_seats=total_seats
    )