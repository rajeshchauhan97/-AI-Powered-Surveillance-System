# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.models.database import SessionLocal, engine, create_tables, Base
from app.routers import movies, theaters, bookings, analytics, shows

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Booking System API - Algo Bharat Assignment",
    description="Complete movie ticket booking system with seat management, group booking, and analytics",
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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
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
        "features": [
            "CRUD operations for movies, theaters, shows",
            "Theater hall layout management with flexible seating",
            "Group booking with seat validation",
            "Alternative show suggestions",
            "Concurrent booking prevention",
            "Analytics APIs"
        ],
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Render"}

# For Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)