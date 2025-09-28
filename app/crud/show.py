# app/crud/show.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.database import Show, Movie, TheaterHall, Theater
from app.schemas.movie import ShowCreate
from typing import List, Optional
from datetime import datetime

def create_show(db: Session, show: ShowCreate):
    db_show = Show(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

def get_show(db: Session, show_id: int):
    return db.query(Show).filter(Show.id == show_id).first()

def get_shows_by_movie(db: Session, movie_id: int):
    return db.query(Show).filter(Show.movie_id == movie_id).all()

def get_shows_by_theater(db: Session, theater_id: int):
    return db.query(Show).join(TheaterHall).filter(TheaterHall.theater_id == theater_id).all()

def get_available_shows(db: Session, movie_id: Optional[int] = None, theater_id: Optional[int] = None):
    query = db.query(Show).join(Movie).join(TheaterHall)
    
    if movie_id:
        query = query.filter(Show.movie_id == movie_id)
    
    if theater_id:
        query = query.filter(TheaterHall.theater_id == theater_id)
    
    # Filter shows that haven't started yet
    query = query.filter(Show.start_time > datetime.now())
    
    return query.all()

def get_shows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Show).offset(skip).limit(limit).all()

def update_show(db: Session, show_id: int, show_data: dict):
    db_show = db.query(Show).filter(Show.id == show_id).first()
    if db_show:
        for key, value in show_data.items():
            setattr(db_show, key, value)
        db.commit()
        db.refresh(db_show)
    return db_show

def delete_show(db: Session, show_id: int):
    db_show = db.query(Show).filter(Show.id == show_id).first()
    if db_show:
        db.delete(db_show)
        db.commit()
    return db_show