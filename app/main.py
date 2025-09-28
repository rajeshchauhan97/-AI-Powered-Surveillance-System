# main.py - Simple FastAPI app for Render
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Movie Booking System API",
    description="Algo Bharat Assignment - Complete Movie Ticket Booking",
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

@app.get("/")
def root():
    return {
        "message": "Movie Booking System API - Algo Bharat Assignment",
        "status": "live",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api": "All CRUD endpoints available"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "Render"}

# Add your other endpoints here temporarily
@app.get("/api/movies")
def get_movies():
    return {"message": "Movies endpoint - Add your actual logic"}

@app.get("/api/theaters")
def get_theaters():
    return {"message": "Theaters endpoint - Add your actual logic"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)