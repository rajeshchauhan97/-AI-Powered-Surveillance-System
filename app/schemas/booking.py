from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any

class BookingBase(BaseModel):
    show_id: int
    user_ids: List[int]
    seats: List[str]

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    booking_id: str
    total_amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class GroupBookingRequest(BaseModel):
    show_id: int
    user_ids: List[int]
    seats: List[str]

class GroupBookingResponse(BaseModel):
    success: bool
    booking: Optional[BookingResponse] = None
    message: str
    alternative_suggestions: List[Dict[str, Any]]