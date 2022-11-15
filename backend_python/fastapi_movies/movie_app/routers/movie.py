from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from sqlalchemy.orm import Session

from movie_app.crud.crud import  crud_update_movie_data, crud_create_new_movie, crud_get_movies, crud_get_movies_by_genre
from movie_app.db.database import SessionLocal
from movie_app.models.models import Movie
from movie_app.schemas.movie import MovieSchemaOutGet, MovieSchemaPost, MovieUpdate, MovieByGenre

movie_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@movie_router.get("/", response_model=List[MovieSchemaOutGet])
def get_all_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        movies = crud_get_movies(db=db, skip=skip, limit=limit)
        return movies
    except ValueError:
        raise HTTPException(status_code=404, detail='Something went wrong!')

@movie_router.post('/new_movie', response_model=MovieSchemaOutGet)
def create_new_movie(new_movie: MovieSchemaPost, db: Session = Depends(get_db)):
    return crud_create_new_movie(db=db, new_movie=new_movie)


@movie_router.put("/{movie_id}", response_model=MovieSchemaOutGet)
def update_movie_by_id(new_movie: MovieUpdate, db: Session = Depends(get_db), movie_id: int = Field(description='Enter '
                                                                                                          'Movie ID')):
    return crud_update_movie_data(movie_id=movie_id, new_movie=new_movie, db=db)


@movie_router.delete('/{movie_id}')
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {f"Movie with id = {movie_id} has been removed!"}



@movie_router.get('/{genre_name}', response_model=MovieByGenre)
def get_movies_by_genre(genre_name: str, db: Session = Depends(get_db)):
    return crud_get_movies_by_genre(genre_name=genre_name,db=db)

