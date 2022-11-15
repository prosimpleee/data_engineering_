from fastapi import HTTPException, Query
from pydantic import Field
from sqlalchemy.orm import Session, joinedload

from movie_app.models.models import Movie, genre_movie, actors_movie, Actor, Director, Genre
from movie_app.schemas.movie import MovieUpdate, MovieSchemaPost, MovieByGenre


def crud_get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Movie).options(joinedload(Movie.actors)) \
        .options(joinedload(Movie.genres)) \
        .options(joinedload(Movie.director)) \
        .offset(skip) \
        .limit(limit) \
        .all()


def crud_create_new_movie(db: Session, new_movie: MovieSchemaPost):
    try:
        db_post_movie = Movie(name=new_movie.name, premiere=new_movie.premiere,
                              description=new_movie.description,
                              director_id=new_movie.director.id)

        db.add(db_post_movie)
        db.commit()
        db.refresh(db_post_movie)

        for genre in new_movie.genres:
            db_post_genre = genre_movie.insert().values(genre_id=genre.id, movie_id=db_post_movie.id)
            db.execute(db_post_genre)
            db.commit()

        for actor in new_movie.actors:
            db_post_actor = actors_movie.insert().values(actor_id=actor.id, movie_id=db_post_movie.id)
            db.execute(db_post_actor)
            db.commit()

        return db_post_movie
    except ValueError:
        raise HTTPException(status_code=404, detail='Something went wrong!')


def crud_get_actors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Actor) \
        .offset(skip) \
        .limit(limit) \
        .all()


def crud_create_actor(first_name: str, last_name: str, db: Session):
    new_actor = Actor(first_name=first_name, last_name=last_name)
    db.add(new_actor)
    db.commit()
    db.refresh(new_actor)
    return new_actor



def crud_update_movie_data(movie_id: int, new_movie: MovieUpdate, db: Session):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).one_or_none()
    if db_movie is None:
        raise HTTPException(status_code=404, detail=f'Movie by {movie_id} not found!')

    try:
        for var, value in vars(new_movie).items():
            setattr(db_movie, var, value) if value else None

        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    except ValueError:
        raise HTTPException(status_code=400, detail='Something went wrong!')


def crud_get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Genre) \
        .offset(skip) \
        .limit(limit) \
        .all()


def crud_create_genre(db: Session, genre: str):
    new_genre = Genre(name=genre)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre


def crud_get_directors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Director) \
        .offset(skip) \
        .limit(limit) \
        .all()


def crud_create_director(fist_name: str, last_name: str, db: Session):
    new_director = Director(first_name=fist_name, last_name=last_name)
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return new_director


def crud_get_movies_by_genre(genre_name: str, db: Session):
    our_genre_id = db.query(Genre).filter(Genre.name == genre_name).first().id
    data = db.query(Genre.name, Movie.name, Movie.premiere, Movie.description).join(genre_movie,
                                                                                    Genre.id == our_genre_id).join(
        Movie, genre_movie.c.movie_id == Movie.id).all()
    return MovieByGenre(genre_name=data[0][0], movies=data)