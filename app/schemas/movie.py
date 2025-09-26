# app/schemas/movie.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    release_date: Optional[datetime] = None

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ShowBase(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    end_time: datetime
    price: float

class ShowCreate(ShowBase):
    pass

class Show(ShowBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True