# app/routers/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta

from app.models import Booking, Show, Movie, Theater
from app.utils.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/movie/{movie_id}/stats")
def get_movie_stats(
    movie_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    # Query bookings for the movie in the date range
    stats = db.query(
        func.count(Booking.id).label("total_bookings"),
        func.sum(Booking.total_amount).label("total_revenue"),
        func.count(func.distinct(Booking.user_id)).label("unique_customers")
    ).join(Show).filter(
        and_(
            Show.movie_id == movie_id,
            Booking.created_at >= start_date,
            Booking.created_at <= end_date,
            Booking.booking_status == "confirmed"
        )
    ).first()
    
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {
        "movie_id": movie_id,
        "movie_title": movie.title,
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "stats": {
            "total_bookings": stats.total_bookings or 0,
            "total_revenue": float(stats.total_revenue or 0),
            "unique_customers": stats.unique_customers or 0
        }
    }

@router.get("/theater/{theater_id}/revenue")
def get_theater_revenue(
    theater_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    # Revenue by movie for the theater
    revenue_by_movie = db.query(
        Movie.title,
        func.count(Booking.id).label("booking_count"),
        func.sum(Booking.total_amount).label("revenue")
    ).select_from(Booking).join(Show).join(Movie).filter(
        and_(
            Show.theater_id == theater_id,
            Booking.created_at >= start_date,
            Booking.created_at <= end_date,
            Booking.booking_status == "confirmed"
        )
    ).group_by(Movie.id, Movie.title).all()
    
    return {
        "theater_id": theater_id,
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "revenue_by_movie": [
            {
                "movie_title": item.title,
                "booking_count": item.booking_count,
                "revenue": float(item.revenue or 0)
            }
            for item in revenue_by_movie
        ]
    }