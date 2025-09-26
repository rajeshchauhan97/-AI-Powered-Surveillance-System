# app/routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.booking import BookingRequest, BookingResponse, BookingSuggestions
from app.crud.booking import create_booking, find_alternative_shows
from app.utils.database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/book", response_model=BookingResponse)
def book_tickets(booking_request: BookingRequest, db: Session = Depends(get_db)):
    booking, error = create_booking(db, booking_request)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Format response
    booked_seats = [
        {"row_number": bs.seat.row_number, "seat_number": bs.seat.seat_number}
        for bs in booking.seats
    ]
    
    return BookingResponse(
        booking_id=booking.id,
        booking_reference=booking.booking_reference,
        total_amount=booking.total_amount,
        booked_seats=booked_seats,
        status=booking.booking_status
    )

@router.post("/book-together", response_model=BookingSuggestions)
def book_tickets_together(booking_request: BookingRequest, db: Session = Depends(get_db)):
    # Try to book original show first
    booking, error = create_booking(db, booking_request)
    
    if not error:
        # Booking successful
        return BookingSuggestions(
            original_show_unavailable=False,
            suggestions=[]
        )
    
    # If original show booking failed, find alternatives
    group_size = len(booking_request.seat_selections)
    suggestions = find_alternative_shows(db, booking_request.show_id, group_size)
    
    return BookingSuggestions(
        original_show_unavailable=True,
        suggestions=suggestions
    )