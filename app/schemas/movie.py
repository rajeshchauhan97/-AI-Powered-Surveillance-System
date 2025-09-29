from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MovieBase(BaseModel):
    title: str
    duration: int
    genre: str
    rating: float

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None

class ShowBase(BaseModel):
    movie_id: int
    theater_id: int
    hall_id: int
    show_time: datetime
    price: float

class ShowCreate(ShowBase):
    pass

class ShowResponse(ShowBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True