from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class TheaterBase(BaseModel):
    name: str
    location: str

class TheaterCreate(TheaterBase):
    pass

class TheaterResponse(TheaterBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class HallBase(BaseModel):
    theater_id: int
    hall_number: int
    seats_per_row: Dict[str, int]  # {"A": 8, "B": 7, ...}

class HallCreate(HallBase):
    pass

class HallResponse(HallBase):
    id: int
    total_rows: int
    created_at: datetime
    
    class Config:
        from_attributes = True