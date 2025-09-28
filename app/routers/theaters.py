# app/routers/theaters.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.theater import Theater, TheaterCreate, TheaterHall, TheaterHallCreate
from app.crud.theater import create_theater, get_theater, get_theaters, create_theater_hall, get_theater_halls, get_hall_layout
from app.utils.database import get_db

router = APIRouter(prefix="/theaters", tags=["theaters"])

@router.post("/", response_model=Theater)
def create_new_theater(theater: TheaterCreate, db: Session = Depends(get_db)):
    return create_theater(db=db, theater=theater)

@router.get("/", response_model=List[Theater])
def read_theaters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    theaters = get_theaters(db, skip=skip, limit=limit)
    return theaters

@router.get("/{theater_id}", response_model=Theater)
def read_theater(theater_id: int, db: Session = Depends(get_db)):
    db_theater = get_theater(db, theater_id=theater_id)
    if db_theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return db_theater

@router.post("/halls/", response_model=TheaterHall)
def create_hall(hall: TheaterHallCreate, db: Session = Depends(get_db)):
    return create_theater_hall(db=db, hall=hall)

@router.get("/{theater_id}/halls/", response_model=List[TheaterHall])
def read_theater_halls(theater_id: int, db: Session = Depends(get_db)):
    return get_theater_halls(db, theater_id=theater_id)

@router.get("/halls/{hall_id}/layout")
def get_hall_seat_layout(hall_id: int, db: Session = Depends(get_db)):
    layout = get_hall_layout(db, hall_id=hall_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Hall not found")
    return layout