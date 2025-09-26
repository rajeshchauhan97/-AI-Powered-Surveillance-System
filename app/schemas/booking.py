# app/schemas/booking.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SeatSelection(BaseModel):
    row_number: int
    seat_number: int

class BookingRequest(BaseModel):
    show_id: int
    seat_selections: List[SeatSelection]

class BookingResponse(BaseModel):
    booking_id: int
    booking_reference: str
    total_amount: float
    booked_seats: List[SeatSelection]
    status: str

class AlternativeShow(BaseModel):
    show_id: int
    movie_title: str
    theater_name: str
    hall_name: str
    start_time: datetime
    available_seats_together: int

class BookingSuggestions(BaseModel):
    original_show_unavailable: bool
    suggestions: List[AlternativeShow]