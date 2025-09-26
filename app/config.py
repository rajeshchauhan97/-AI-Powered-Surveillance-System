# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Railway provides DATABASE_URL environment variable
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./movie_booking.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()