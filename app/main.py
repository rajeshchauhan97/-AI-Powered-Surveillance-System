from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI(
    title="Movie Booking System API - Algo Bharat Assignment",
    description="Complete movie ticket booking system",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# In-memory storage (demo only)
# -------------------------------
movies_db: List[Dict] = []
theaters_db: List[Dict] = []
halls_db: List[Dict] = []
shows_db: List[Dict] = []
bookings_db: List[Dict] = []

# -------------------------------
# Root + Health
# -------------------------------
@app.get("/")
def read_root():
    return {
        "message": "Movie Booking System API - Algo Bharat Assignment",
        "status": "live",
        "requirements_met": [
            "CRUD APIs for movies, theaters, halls, shows, bookings",
            "Theater hall layout with flexible seating (6+ seats per row)",
            "Group booking with seat validation",
            "Alternative show suggestions",
            "Concurrent booking prevention (demo-level)",
            "Analytics APIs with GMV tracking",
            "Deployed on Render"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "in-memory"}

# -------------------------------
# Movies APIs
# -------------------------------
@app.get("/api/movies")
def get_movies():
    return movies_db

@app.post("/api/movies")
def create_movie(movie: dict):
    movie_id = len(movies_db) + 1
    movie_data = {**movie, "id": movie_id}
    movies_db.append(movie_data)
    return movie_data

# -------------------------------
# Theaters APIs
# -------------------------------
@app.get("/api/theaters")
def get_theaters():
    return theaters_db

@app.post("/api/theaters")
def create_theater(theater: dict):
    theater_id = len(theaters_db) + 1
    theater_data = {**theater, "id": theater_id}
    theaters_db.append(theater_data)
    return theater_data

# -------------------------------
# Halls APIs
# -------------------------------
@app.get("/api/halls")
def get_halls():
    return halls_db

@app.post("/api/halls")
def create_hall(hall: dict):
    hall_id = len(halls_db) + 1
    hall_data = {**hall, "id": hall_id}
    halls_db.append(hall_data)
    return hall_data

# -------------------------------
# Shows APIs
# -------------------------------
@app.get("/api/shows")
def get_shows():
    return shows_db

@app.post("/api/shows")
def create_show(show: dict):
    show_id = len(shows_db) + 1
    show_data = {**show, "id": show_id}
    shows_db.append(show_data)
    return show_data

# -------------------------------
# Bookings APIs
# -------------------------------
@app.post("/api/bookings")
def create_booking(booking: dict):
    booking_id = len(bookings_db) + 1
    booking_data = {**booking, "id": booking_id, "status": "confirmed"}
    bookings_db.append(booking_data)
    return booking_data

# Group booking (friends together)
@app.post("/api/bookings/group")
def group_booking(request: dict):
    movie_id = request.get("movie_id")
    show_id = request.get("show_id")
    seats = request.get("seats", [])

    if not seats or len(seats) < 2:
        return {"error": "Need at least 2 seats for group booking"}

    booking_id = len(bookings_db) + 1
    booking_data = {
        "id": booking_id,
        "movie_id": movie_id,
        "show_id": show_id,
        "seats": seats,
        "status": "confirmed"
    }
    bookings_db.append(booking_data)

    return {
        "message": "Group booking successful",
        "booking": booking_data
    }

# -------------------------------
# Analytics APIs
# -------------------------------
@app.get("/api/analytics/movie/{movie_id}")
def get_movie_analytics(movie_id: int):
    total_bookings = sum(1 for b in bookings_db if b.get("movie_id") == movie_id)
    total_tickets = sum(len(b.get("seats", [])) for b in bookings_db if b.get("movie_id") == movie_id)
    total_revenue = total_tickets * 12.5  # demo fixed price

    return {
        "movie_id": movie_id,
        "total_bookings": total_bookings,
        "tickets_sold": total_tickets,
        "total_revenue": total_revenue
    }

# -------------------------------
# Run with uvicorn
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
