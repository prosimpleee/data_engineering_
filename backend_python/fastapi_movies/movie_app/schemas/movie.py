from typing import List, Dict

from pydantic import BaseModel
from datetime import date

from movie_app.schemas.actor import ActorCreate
from movie_app.schemas.genre import GenresCreate

from movie_app.schemas.actor import ActorBase
from movie_app.schemas.genre import GenreBase
from movie_app.schemas.director import DirectorBase, DirectorCreate


class MovieBase(BaseModel):
    name: str
    premiere: date
    description: str

    class Config:
        orm_mode = True


class MovieSchemaPost(MovieBase):
    actors: List[ActorCreate]
    genres: List[GenresCreate]
    director: DirectorCreate

    class Config:
        schema_extra = {
            "example": {
                "name": "Gandhi",
                "premiere": "1982-11-30",
                "description": "The life of the lawyer who became the famed leader..",
                "actors": [
                    {
                        "id": 2
                    },
                    {
                        "id": 35
                    }
                ],
                "genres": [
                    {
                        "id": 4
                    }
                ],
                "director": {
                    "id": 23
                }
            }
        }


class MovieSchemaOutGet(MovieBase):
    director: DirectorBase
    actors: List[ActorBase]
    genres: List[GenreBase]


class MovieUpdate(MovieBase):
    director_id: int


class MovieByGenre(BaseModel):
    genre_name: str
    movies: List[MovieBase]
