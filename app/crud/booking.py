# app/crud/booking.py
from sqlalchemy.orm import Session, load_only
from sqlalchemy import and_, or_, text
from app.models import Booking, Show, Seat, BookingSeat, TheaterHall, Movie
from app.schemas.booking import BookingRequest, SeatSelection
from datetime import datetime, timedelta
import uuid
from typing import List, Tuple

def create_booking(db: Session, booking_request: BookingRequest, user_id: int = 1):
    # Start transaction
    try:
        # Generate unique booking reference
        booking_ref = str(uuid.uuid4())[:8].upper()
        
        # Get show details
        show = db.query(Show).filter(Show.id == booking_request.show_id).first()
        if not show:
            return None, "Show not found"
        
        # Check seat availability and lock seats
        unavailable_seats = []
        seats_to_book = []
        total_amount = 0
        
        for seat_req in booking_request.seat_selections:
            seat = db.query(Seat).filter(
                and_(
                    Seat.hall_id == show.hall_id,
                    Seat.row_number == seat_req.row_number,
                    Seat.seat_number == seat_req.seat_number
                )
            ).first()
            
            if not seat:
                unavailable_seats.append(seat_req)
                continue
            
            # Check if seat is already booked
            existing_booking = db.query(BookingSeat).join(Booking).filter(
                and_(
                    BookingSeat.seat_id == seat.id,
                    Booking.show_id == show.id,
                    Booking.booking_status == "confirmed"
                )
            ).first()
            
            if existing_booking:
                unavailable_seats.append(seat_req)
            else:
                seats_to_book.append(seat)
                total_amount += show.price
        
        if unavailable_seats:
            return None, f"Seats unavailable: {unavailable_seats}"
        
        # Create booking
        booking = Booking(
            show_id=booking_request.show_id,
            user_id=user_id,
            booking_reference=booking_ref,
            total_amount=total_amount,
            booking_status="confirmed"
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        # Create booking-seat associations
        for seat in seats_to_book:
            booking_seat = BookingSeat(booking_id=booking.id, seat_id=seat.id)
            db.add(booking_seat)
        
        db.commit()
        return booking, None
        
    except Exception as e:
        db.rollback()
        return None, str(e)

def find_alternative_shows(db: Session, original_show_id: int, group_size: int):
    original_show = db.query(Show).filter(Show.id == original_show_id).first()
    if not original_show:
        return []
    
    # Find shows around the same time (±3 hours)
    time_window_start = original_show.start_time - timedelta(hours=3)
    time_window_end = original_show.start_time + timedelta(hours=3)
    
    alternative_shows = db.query(Show).join(Movie).join(TheaterHall).filter(
        and_(
            Show.start_time >= time_window_start,
            Show.start_time <= time_window_end,
            Show.id != original_show_id
        )
    ).all()
    
    suggestions = []
    for show in alternative_shows:
        # Check for consecutive seats
        available_together = find_consecutive_seats(db, show.id, group_size)
        if available_together >= group_size:
            suggestions.append({
                "show_id": show.id,
                "movie_title": show.movie.title,
                "theater_name": show.hall.theater.name,
                "hall_name": show.hall.name,
                "start_time": show.start_time,
                "available_seats_together": available_together
            })
    
    return suggestions

def find_consecutive_seats(db: Session, show_id: int, required_count: int):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        return 0
    
    # Get all seats for the hall
    seats = db.query(Seat).filter(Seat.hall_id == show.hall_id).order_by(
        Seat.row_number, Seat.seat_number
    ).all()
    
    # Group seats by row
    seats_by_row = {}
    for seat in seats:
        if seat.row_number not in seats_by_row:
            seats_by_row[seat.row_number] = []
        seats_by_row[seat.row_number].append(seat)
    
    max_consecutive = 0
    
    for row_num, row_seats in seats_by_row.items():
        # Sort seats by seat number
        row_seats.sort(key=lambda x: x.seat_number)
        
        # Check booked seats
        booked_seat_ids = set()
        bookings = db.query(BookingSeat.seat_id).join(Booking).filter(
            and_(
                Booking.show_id == show_id,
                Booking.booking_status == "confirmed"
            )
        ).all()
        booked_seat_ids.update([b.seat_id for b in bookings])
        
        # Find consecutive available seats
        current_streak = 0
        for seat in row_seats:
            if seat.id not in booked_seat_ids:
                current_streak += 1
                max_consecutive = max(max_consecutive, current_streak)
                if max_consecutive >= required_count:
                    return max_consecutive
            else:
                current_streak = 0
    
    return max_consecutive