# app/crud/show.py
from sqlalchemy.orm import Session
from app.models import Show
from app.schemas.movie import ShowCreate
from typing import List, Optional
from datetime import datetime

def get_show(db: Session, show_id: int):
    return db.query(Show).filter(Show.id == show_id).first()

def get_shows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Show).offset(skip).limit(limit).all()

def get_shows_by_movie(db: Session, movie_id: int):
    return db.query(Show).filter(Show.movie_id == movie_id).all()

def get_shows_by_theater(db: Session, theater_id: int):
    return db.query(Show).join(Show.hall).filter(Show.hall.theater_id == theater_id).all()

def create_show(db: Session, show: ShowCreate):
    db_show = Show(**show.model_dump())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

def update_show(db: Session, show_id: int, show_data: dict):
    db_show = db.query(Show).filter(Show.id == show_id).first()
    if db_show:
        for field, value in show_data.items():
            setattr(db_show, field, value)
        db.commit()
        db.refresh(db_show)
    return db_show

def delete_show(db: Session, show_id: int):
    db_show = db.query(Show).filter(Show.id == show_id).first()
    if db_show:
        db.delete(db_show)
        db.commit()
        return True
    return False