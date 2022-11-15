from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from movie_app.crud.crud import crud_get_actors, crud_create_actor
from movie_app.db.database import SessionLocal
from movie_app.schemas.actor import ActorGet


actor_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@actor_router.get('/', response_model=List[ActorGet])
def get_query_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip >= limit:
        raise HTTPException(status_code=404, detail="Skip greater than than limit! Check your data")
    actors = crud_get_actors(db=db, skip=skip, limit=limit)
    return actors


@actor_router.post('/new_actor', response_model=ActorGet)
def create_actor(first_name: str = Query(alias='First name'), last_name: str = Query(alias='Last name'), db: Session = Depends(get_db)):
    return crud_create_actor(first_name=first_name, last_name=last_name, db=db)
