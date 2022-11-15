from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from movie_app.crud.crud import crud_create_director, crud_get_directors
from movie_app.db.database import SessionLocal
from movie_app.schemas.director import DirectorSchemaOut

directors_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@directors_router.get('/', response_model=List[DirectorSchemaOut])
def get_query_directors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip >= limit:
        raise HTTPException(status_code=404, detail="Skip greater than than limit! Check your data")
    directors = crud_get_directors(db=db, skip=skip, limit=limit)
    return directors


@directors_router.post('/new_director', response_model=DirectorSchemaOut)
def create_director(first_name: str = Query(alias='First name'),last_name : str = Query(alias='Last name'),  db: Session = Depends(get_db)):
    return crud_create_director(fist_name=first_name, last_name=last_name, db=db)