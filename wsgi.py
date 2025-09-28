# wsgi.py - WSGI entry point for Render
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
except ImportError:
    # Fallback: create simple app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    def root():
        return {"message": "Movie Booking System - WSGI Mode"}

# WSGI application
application = app