# app/routers/shows.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.schemas.movie import Show, ShowCreate
from app.crud.show import get_show, get_shows, create_show, update_show, delete_show, get_shows_by_movie, get_shows_by_theater
from app.utils.database import get_db

router = APIRouter(prefix="/shows", tags=["shows"])

@router.get("/", response_model=List[Show])
def read_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shows = get_shows(db, skip=skip, limit=limit)
    return shows

@router.get("/{show_id}", response_model=Show)
def read_show(show_id: int, db: Session = Depends(get_db)):
    db_show = get_show(db, show_id=show_id)
    if db_show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return db_show

@router.get("/movie/{movie_id}", response_model=List[Show])
def read_shows_by_movie(movie_id: int, db: Session = Depends(get_db)):
    shows = get_shows_by_movie(db, movie_id=movie_id)
    return shows

@router.get("/theater/{theater_id}", response_model=List[Show])
def read_shows_by_theater(theater_id: int, db: Session = Depends(get_db)):
    shows = get_shows_by_theater(db, theater_id=theater_id)
    return shows

@router.post("/", response_model=Show)
def create_new_show(show: ShowCreate, db: Session = Depends(get_db)):
    return create_show(db=db, show=show)

@router.put("/{show_id}", response_model=Show)
def update_existing_show(show_id: int, show: ShowCreate, db: Session = Depends(get_db)):
    db_show = update_show(db=db, show_id=show_id, show_data=show.model_dump())
    if db_show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return db_show

@router.delete("/{show_id}")
def delete_existing_show(show_id: int, db: Session = Depends(get_db)):
    success = delete_show(db=db, show_id=show_id)
    if not success:
        raise HTTPException(status_code=404, detail="Show not found")
    return {"message": "Show deleted successfully"}