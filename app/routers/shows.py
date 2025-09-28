from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.schemas.movie import Show, ShowCreate
from app.crud.show import create_show, get_shows_by_movie, get_available_shows
from app.utils.database import get_db

router = APIRouter(prefix="/shows", tags=["shows"])

@router.post("/", response_model=Show)
def create_movie_show(show: ShowCreate, db: Session = Depends(get_db)):
    return create_show(db=db, show=show)

@router.get("/movie/{movie_id}", response_model=List[Show])
def get_movie_shows(movie_id: int, db: Session = Depends(get_db)):
    return get_shows_by_movie(db, movie_id=movie_id)

@router.get("/available")
def get_available_movie_shows(movie_id: int = None, theater_id: int = None, db: Session = Depends(get_db)):
    return get_available_shows(db, movie_id=movie_id, theater_id=theater_id)