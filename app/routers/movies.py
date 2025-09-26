# app/routers/movies.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.movie import Movie, MovieCreate, MovieUpdate
from app.crud.movie import get_movie, get_movies, create_movie, update_movie, delete_movie
from app.utils.database import get_db

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=List[Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = get_movies(db, skip=skip, limit=limit)
    return movies

@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.post("/", response_model=Movie)
def create_new_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return create_movie(db=db, movie=movie)

@router.put("/{movie_id}", response_model=Movie)
def update_existing_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = update_movie(db=db, movie_id=movie_id, movie=movie)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.delete("/{movie_id}")
def delete_existing_movie(movie_id: int, db: Session = Depends(get_db)):
    success = delete_movie(db=db, movie_id=movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}