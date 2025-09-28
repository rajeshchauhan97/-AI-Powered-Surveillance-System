# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./movie_booking.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Render specific
    RENDER: bool = False
    
    class Config:
        env_file = ".env"
        extra = 'ignore'

<<<<<<< HEAD
settings = Settings()
=======
settings = Settings()
>>>>>>> 27f58074d1bd026bd7866b0f9bb3fed4f08de75b
