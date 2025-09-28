from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import func

from app.utils.database import get_db
from app.models.database import Booking, Show, Movie, Theater

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/movie/{movie_id}")
def get_movie_analytics(movie_id: int, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    # Default to last 30 days
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
    if not end_date:
        end_date = datetime.now().isoformat()
    
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    # Get movie details
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Calculate analytics
    result = db.query(
        func.count(Booking.id).label("total_bookings"),
        func.sum(Booking.total_amount).label("total_revenue"),
        func.count(func.distinct(Booking.user_id)).label("unique_customers")
    ).join(Show).filter(
        Show.movie_id == movie_id,
        Booking.created_at >= start,
        Booking.created_at <= end,
        Booking.booking_status == "confirmed"
    ).first()
    
    return {
        "movie_id": movie_id,
        "movie_title": movie.title,
        "period": {"start_date": start_date, "end_date": end_date},
        "analytics": {
            "total_bookings": result.total_bookings or 0,
            "total_revenue": float(result.total_revenue or 0),
            "unique_customers": result.unique_customers or 0,
            "average_ticket_price": float(result.total_revenue or 0) / (result.total_bookings or 1)
        }
    }

@router.get("/theater/{theater_id}")
def get_theater_analytics(theater_id: int, db: Session = Depends(get_db)):
    # Revenue by movie for this theater
    revenue_by_movie = db.query(
        Movie.title,
        func.count(Booking.id).label("booking_count"),
        func.sum(Booking.total_amount).label("revenue")
    ).select_from(Booking).join(Show).join(Movie).filter(
        Show.theater_id == theater_id,
        Booking.booking_status == "confirmed"
    ).group_by(Movie.id, Movie.title).all()
    
    return {
        "theater_id": theater_id,
        "revenue_breakdown": [
            {
                "movie_title": item.title,
                "booking_count": item.booking_count,
                "revenue": float(item.revenue or 0)
            }
            for item in revenue_by_movie
        ]
    }