# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Use SQLite for simplicity
    DATABASE_URL: str = "sqlite:///./movie_booking.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = Settings()