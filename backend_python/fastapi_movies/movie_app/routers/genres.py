from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Field
from sqlalchemy.orm import Session

from movie_app.crud.crud import crud_get_genres, crud_create_genre
from movie_app.db.database import SessionLocal
from movie_app.schemas.genre import GenreSchemeOut

genres_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@genres_router.get('/', response_model=List[GenreSchemeOut])
def get_query_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip >= limit:
        raise HTTPException(status_code=404, detail="Skip greater than than limit! Check your data")
    genres = crud_get_genres(db=db, skip=skip, limit=limit)
    return genres


@genres_router.post('/new_genre', response_model=GenreSchemeOut)
def create_genre(name: str = Query(alias='Enter genre'), db: Session = Depends(get_db)):
    return crud_create_genre(genre=name, db=db)



