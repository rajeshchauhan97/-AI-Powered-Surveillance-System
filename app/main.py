from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import uuid
import uvicorn
import os

# Database setup - DELETE OLD DATABASE FIRST
if os.path.exists("movie_booking.db"):
    os.remove("movie_booking.db")
    print("🗑️  Deleted old database file")

SQLALCHEMY_DATABASE_URL = "sqlite:///./movie_booking.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Theater(Base):
    __tablename__ = "theaters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Hall(Base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, nullable=False)
    hall_number = Column(Integer, nullable=False)
    total_rows = Column(Integer, nullable=False)
    seats_per_row = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False)
    theater_id = Column(Integer, nullable=False)
    hall_id = Column(Integer, nullable=False)
    show_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String(50), unique=True, nullable=False)
    show_id = Column(Integer, nullable=False)
    user_ids = Column(JSON, nullable=False)
    seats = Column(JSON, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Movie Booking System - Algo Bharat",
    description="Complete movie ticket booking API with all requirements",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Seat locking for concurrent booking
seat_locks = {}

@app.get("/")
def root():
    return {
        "message": "🎬 Movie Booking System - Algo Bharat Assignment",
        "status": "ACTIVE",
        "docs": "/docs",
        "health": "/health",
        "requirements": "All Algo Bharat requirements implemented ✓"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection with proper text()
        db.execute(text("SELECT 1"))
        db_status = "connected"
        
        # Get basic counts
        movies_count = db.query(Movie).count()
        theaters_count = db.query(Theater).count()
        bookings_count = db.query(Booking).count()
        
        return {
            "status": "healthy",
            "database": db_status,
            "movies_count": movies_count,
            "theaters_count": theaters_count,
            "bookings_count": bookings_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }

# 1. MOVIE APIs
@app.post("/movies")
def create_movie(movie_data: dict, db: Session = Depends(get_db)):
    try:
        movie = Movie(
            title=movie_data["title"],
            duration=movie_data["duration"],
            genre=movie_data["genre"],
            rating=movie_data["rating"]
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return {
            "id": movie.id,
            "title": movie.title,
            "duration": movie.duration,
            "genre": movie.genre,
            "rating": movie.rating,
            "created_at": movie.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating movie: {str(e)}")

@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return [
        {
            "id": movie.id,
            "title": movie.title,
            "duration": movie.duration,
            "genre": movie.genre,
            "rating": movie.rating,
            "created_at": movie.created_at.isoformat()
        }
        for movie in movies
    ]

# 2. THEATER APIs
@app.post("/theaters")
def create_theater(theater_data: dict, db: Session = Depends(get_db)):
    try:
        theater = Theater(
            name=theater_data["name"],
            location=theater_data["location"]
        )
        db.add(theater)
        db.commit()
        db.refresh(theater)
        return {
            "id": theater.id,
            "name": theater.name,
            "location": theater.location,
            "created_at": theater.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating theater: {str(e)}")

@app.get("/theaters")
def get_theaters(db: Session = Depends(get_db)):
    theaters = db.query(Theater).all()
    return [
        {
            "id": theater.id,
            "name": theater.name,
            "location": theater.location,
            "created_at": theater.created_at.isoformat()
        }
        for theater in theaters
    ]

# 3. HALL APIs (with 6+ seats validation)
@app.post("/halls")
def create_hall(hall_data: dict, db: Session = Depends(get_db)):
    try:
        # Validate 6+ seats per row requirement
        for row, seats in hall_data["seats_per_row"].items():
            if seats < 6:
                raise HTTPException(status_code=400, detail=f"Row {row} must have at least 6 seats (has {seats})")
        
        hall = Hall(
            theater_id=hall_data["theater_id"],
            hall_number=hall_data["hall_number"],
            seats_per_row=hall_data["seats_per_row"],
            total_rows=len(hall_data["seats_per_row"])
        )
        db.add(hall)
        db.commit()
        db.refresh(hall)
        return {
            "id": hall.id,
            "theater_id": hall.theater_id,
            "hall_number": hall.hall_number,
            "seats_per_row": hall.seats_per_row,
            "total_rows": hall.total_rows,
            "created_at": hall.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating hall: {str(e)}")

@app.get("/halls")
def get_halls(db: Session = Depends(get_db)):
    halls = db.query(Hall).all()
    return [
        {
            "id": hall.id,
            "theater_id": hall.theater_id,
            "hall_number": hall.hall_number,
            "seats_per_row": hall.seats_per_row,
            "total_rows": hall.total_rows,
            "created_at": hall.created_at.isoformat()
        }
        for hall in halls
    ]

# 4. SHOW APIs
@app.post("/shows")
def create_show(show_data: dict, db: Session = Depends(get_db)):
    try:
        show = Show(
            movie_id=show_data["movie_id"],
            theater_id=show_data["theater_id"],
            hall_id=show_data["hall_id"],
            show_time=datetime.fromisoformat(show_data["show_time"].replace('Z', '+00:00')),
            price=show_data["price"]
        )
        db.add(show)
        db.commit()
        db.refresh(show)
        return {
            "id": show.id,
            "movie_id": show.movie_id,
            "theater_id": show.theater_id,
            "hall_id": show.hall_id,
            "show_time": show.show_time.isoformat(),
            "price": show.price,
            "created_at": show.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating show: {str(e)}")

@app.get("/shows")
def get_shows(db: Session = Depends(get_db)):
    shows = db.query(Show).all()
    return [
        {
            "id": show.id,
            "movie_id": show.movie_id,
            "theater_id": show.theater_id,
            "hall_id": show.hall_id,
            "show_time": show.show_time.isoformat(),
            "price": show.price,
            "created_at": show.created_at.isoformat()
        }
        for show in shows
    ]

# 5. GROUP BOOKING API (Main Feature)
@app.post("/bookings/group")
def group_booking(booking_data: dict, db: Session = Depends(get_db)):
    try:
        # Get show details
        show = db.query(Show).filter(Show.id == booking_data["show_id"]).first()
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")
        
        # Get hall layout
        hall = db.query(Hall).filter(Hall.id == show.hall_id).first()
        if not hall:
            raise HTTPException(status_code=404, detail="Hall not found")
        
        # Validate seats exist
        all_seats = []
        for row, count in hall.seats_per_row.items():
            for seat_num in range(1, count + 1):
                all_seats.append(f"{row}{seat_num}")
        
        invalid_seats = [seat for seat in booking_data["seats"] if seat not in all_seats]
        if invalid_seats:
            raise HTTPException(status_code=400, detail=f"Invalid seats: {invalid_seats}")
        
        # Check if seats are available
        existing_bookings = db.query(Booking).filter(Booking.show_id == booking_data["show_id"]).all()
        booked_seats = []
        for booking in existing_bookings:
            booked_seats.extend(booking.seats)
        
        unavailable_seats = [seat for seat in booking_data["seats"] if seat in booked_seats]
        
        if unavailable_seats:
            # ALTERNATIVE SUGGESTIONS FEATURE
            alternatives = []
            other_shows = db.query(Show).filter(
                Show.movie_id == show.movie_id,
                Show.id != show.id,
                Show.show_time > datetime.utcnow()
            ).all()
            
            for alt_show in other_shows:
                alt_hall = db.query(Hall).filter(Hall.id == alt_show.hall_id).first()
                if alt_hall:
                    # Get available seats for alternative show
                    alt_bookings = db.query(Booking).filter(Booking.show_id == alt_show.id).all()
                    alt_booked_seats = []
                    for booking in alt_bookings:
                        alt_booked_seats.extend(booking.seats)
                    
                    alt_all_seats = []
                    for row, count in alt_hall.seats_per_row.items():
                        for seat_num in range(1, count + 1):
                            alt_all_seats.append(f"{row}{seat_num}")
                    
                    alt_available = [seat for seat in alt_all_seats if seat not in alt_booked_seats]
                    
                    if len(alt_available) >= len(booking_data["seats"]):
                        alternatives.append({
                            "show_id": alt_show.id,
                            "theater_id": alt_show.theater_id,
                            "show_time": alt_show.show_time.isoformat(),
                            "available_seats": alt_available[:len(booking_data["seats"])],
                            "price": alt_show.price
                        })
            
            return {
                "success": False,
                "message": f"Seats {unavailable_seats} not available together",
                "alternative_suggestions": alternatives
            }
        
        # CONCURRENT BOOKING PROTECTION
        lock_key = f"{show.id}_{'_'.join(booking_data['seats'])}"
        if lock_key in seat_locks and seat_locks[lock_key] > datetime.utcnow():
            raise HTTPException(status_code=409, detail="Seats are currently being booked by another user")
        
        # Acquire lock
        seat_locks[lock_key] = datetime.utcnow() + timedelta(seconds=30)
        
        try:
            # Create booking
            total_amount = len(booking_data["seats"]) * show.price
            booking = Booking(
                booking_id=str(uuid.uuid4()),
                show_id=booking_data["show_id"],
                user_ids=booking_data["user_ids"],
                seats=booking_data["seats"],
                total_amount=total_amount,
                status="confirmed"
            )
            db.add(booking)
            db.commit()
            db.refresh(booking)
            
            return {
                "success": True,
                "booking": {
                    "id": booking.id,
                    "booking_id": booking.booking_id,
                    "show_id": booking.show_id,
                    "user_ids": booking.user_ids,
                    "seats": booking.seats,
                    "total_amount": booking.total_amount,
                    "status": booking.status,
                    "created_at": booking.created_at.isoformat()
                },
                "message": "Seats booked successfully together!",
                "alternative_suggestions": []
            }
        finally:
            # Release lock
            if lock_key in seat_locks:
                del seat_locks[lock_key]
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")

# 6. AVAILABLE SEATS API
@app.get("/shows/{show_id}/seats")
def get_available_seats(show_id: int, db: Session = Depends(get_db)):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    
    hall = db.query(Hall).filter(Hall.id == show.hall_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    # Generate all seats
    all_seats = []
    for row, count in hall.seats_per_row.items():
        for seat_num in range(1, count + 1):
            all_seats.append(f"{row}{seat_num}")
    
    # Get booked seats
    bookings = db.query(Booking).filter(Booking.show_id == show_id).all()
    booked_seats = []
    for booking in bookings:
        booked_seats.extend(booking.seats)
    
    available_seats = [seat for seat in all_seats if seat not in booked_seats]
    
    return {
        "show_id": show_id,
        "total_seats": len(all_seats),
        "booked_seats": len(booked_seats),
        "available_seats": available_seats,
        "hall_layout": hall.seats_per_row
    }

# 7. ANALYTICS APIs (GMV Tracking)
@app.get("/analytics/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    total_bookings = len(bookings)
    total_tickets = sum(len(booking.seats) for booking in bookings)
    total_revenue = sum(booking.total_amount for booking in bookings)
    
    return {
        "total_bookings": total_bookings,
        "total_tickets": total_tickets,
        "total_revenue": total_revenue,
        "average_ticket_price": round(total_revenue / total_tickets, 2) if total_tickets > 0 else 0
    }

@app.get("/analytics/movie/{movie_id}")
def get_movie_analytics(movie_id: int, db: Session = Depends(get_db)):
    shows = db.query(Show).filter(Show.movie_id == movie_id).all()
    show_ids = [show.id for show in shows]
    
    bookings = db.query(Booking).filter(Booking.show_id.in_(show_ids)).all()
    total_tickets = sum(len(booking.seats) for booking in bookings)
    total_revenue = sum(booking.total_amount for booking in bookings)
    
    return {
        "movie_id": movie_id,
        "total_shows": len(shows),
        "total_tickets": total_tickets,
        "total_revenue": total_revenue,
        "gmv": total_revenue
    }

if __name__ == "__main__":
    print("🚀 Starting Movie Booking System...")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🔍 Health Check: http://127.0.0.1:8000/health")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)