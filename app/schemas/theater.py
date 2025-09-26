# app/schemas/theater.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class TheaterBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class TheaterCreate(TheaterBase):
    pass

class Theater(TheaterBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SeatLayout(BaseModel):
    row_number: int
    total_seats: int  # Must be at least 6

class TheaterHallBase(BaseModel):
    theater_id: int
    name: str
    layout: List[SeatLayout]  # List of rows with seat counts

class TheaterHallCreate(TheaterHallBase):
    pass

class TheaterHall(TheaterHallBase):
    id: int
    total_seats: int
    
    class Config:
        from_attributes = True