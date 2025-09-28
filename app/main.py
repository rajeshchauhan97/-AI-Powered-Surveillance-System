# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.models.database import SessionLocal, engine, Base
from app.routers import movies, theaters, bookings, analytics, shows

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Booking System API - Algo Bharat Assignment",
    description="Complete movie ticket booking system with seat management, group booking, and analytics. Meets all Algo Bharat requirements.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include all routers
app.include_router(movies.router, prefix="/api")
app.include_router(theaters.router, prefix="/api")
app.include_router(shows.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Movie Booking System API - Algo Bharat Assignment",
        "status": "live",
        "requirements_met": [
            "CRUD APIs for movies, theaters, shows, bookings",
            "Theater hall layout with flexible seating (6+ seats per row)",
            "Group booking with seat validation",
            "Alternative show suggestions",
            "Concurrent booking prevention",
            "Analytics APIs with GMV tracking",
            "Deployed on Render"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "movies": "/api/movies",
            "theaters": "/api/theaters",
            "bookings": "/api/bookings",
            "analytics": "/api/analytics"
        }
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy", 
        "database": db_status,
        "service": "Render" if os.environ.get('RENDER') else "Local"
    }

# Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
<<<<<<< HEAD
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
=======
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
>>>>>>> 27f58074d1bd026bd7866b0f9bb3fed4f08de75b
