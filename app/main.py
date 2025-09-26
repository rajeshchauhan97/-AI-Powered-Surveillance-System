import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import your routers and database setup
from app.routers import movies, theaters, bookings, analytics, shows
from app.utils.database import get_db, check_database_health
from app.models.database import create_tables

# Create tables on startup
create_tables()

# Get port from Render environment
PORT = int(os.environ.get("PORT", 8000))

app = FastAPI(
    title="Movie Booking System API",
    description="Algo Bharat Assignment - Complete Movie Ticket Booking System",
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

# Include routers
app.include_router(movies.router, prefix="/api/v1", tags=["movies"])
app.include_router(theaters.router, prefix="/api/v1", tags=["theaters"])
app.include_router(shows.router, prefix="/api/v1", tags=["shows"])
app.include_router(bookings.router, prefix="/api/v1", tags=["bookings"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])

@app.get("/")
def root():
    return {
        "message": "Movie Booking System API - Algo Bharat Assignment",
        "status": "live",
        "deployed_on": "Render.com",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db_healthy, db_error = check_database_health(db)
        return {
            "status": "healthy" if db_healthy else "unhealthy",
            "database": "connected" if db_healthy else "disconnected",
            "service": "Render",
            "error": db_error
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)