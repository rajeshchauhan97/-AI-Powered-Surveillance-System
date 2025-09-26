# app/main.py
import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routers import movies, theaters, bookings, analytics, shows
from app.utils.database import get_db, check_database_health
from app.models.database import create_tables

# Create tables on startup
create_tables()

# Get port from Railway environment
PORT = int(os.environ.get("PORT", 8000))

app = FastAPI(
    title="Movie Booking System API", 
    version="1.0.0",
    description="Algo Bharat Assignment - Movie Ticket Booking System"
)

# CORS middleware for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(theaters.router)
app.include_router(shows.router)
app.include_router(bookings.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {
        "message": "Movie Booking System API - Algo Bharat Assignment",
        "status": "live",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_healthy, db_error = check_database_health(db)
    status = "healthy" if db_healthy else "unhealthy"
    return {
        "status": status, 
        "database": "connected" if db_healthy else "disconnected",
        "error": db_error if not db_healthy else None,
        "service": "Railway"
    }

@app.on_event("startup")
async def startup_event():
    print("🚀 Movie Booking System deployed on Railway!")
    print("📚 API Documentation: /docs")
    print("❤️ Health Check: /health")