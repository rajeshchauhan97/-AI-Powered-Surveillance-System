# render_app.py - Simple FastAPI app for Render
from fastapi import FastAPI

app = FastAPI(title="Movie Booking System")

@app.get("/")
def root():
    return {"message": "Movie Booking API - Algo Bharat Assignment"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/docs")
def docs_info():
    return {"message": "API documentation available"}

# Add your actual endpoints here
@app.get("/api/movies")
def get_movies():
    return {"endpoint": "movies", "status": "working"}

@app.get("/api/theaters")
def get_theaters():
    return {"endpoint": "theaters", "status": "working"}
