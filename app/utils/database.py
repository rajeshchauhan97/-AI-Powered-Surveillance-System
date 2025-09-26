# app/utils/database.py
from sqlalchemy import text
from app.models.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database_health(db):
    """Check if database connection is healthy"""
    try:
        # Use text() for explicit SQL expressions in SQLAlchemy 2.0
        db.execute(text("SELECT 1"))
        return True, "connected"
    except Exception as e:
        return False, str(e)