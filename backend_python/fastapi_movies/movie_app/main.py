from fastapi import FastAPI
from movie_app.db.database import engine
from movie_app.models.models import Base
from movie_app.routers.actors import actor_router
from movie_app.routers.director import directors_router
from movie_app.routers.movie import movie_router
from movie_app.routers.genres import genres_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(movie_router, prefix="/movies", tags=['Movies'])
app.include_router(actor_router, prefix='/actors', tags=['Actors'])
app.include_router(genres_router, prefix='/genres', tags=['Genres'])
app.include_router(directors_router, prefix='/directors', tags=['Directors'])
