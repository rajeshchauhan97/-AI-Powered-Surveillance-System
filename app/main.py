# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routers import movies, theaters, bookings, analytics, shows  # Add shows
from app.utils.database import get_db, check_database_health
from app.models.database import create_tables

# Create tables on startup
create_tables()

app = FastAPI(title="Movie Booking System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(theaters.router)
app.include_router(shows.router)  # Add this line
app.include_router(bookings.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Movie Booking System API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_healthy, db_error = check_database_health(db)
    status = "healthy" if db_healthy else "unhealthy"
    return {
        "status": status, 
        "database": "connected" if db_healthy else "disconnected",
        "error": db_error if not db_healthy else None
    }

@app.on_event("startup")
async def startup_event():
    print("Movie Booking System API started successfully!")
    print("Access the API documentation at: http://localhost:8000/docs")