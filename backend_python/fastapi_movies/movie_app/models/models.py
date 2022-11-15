from sqlalchemy import Text, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.testing.schema import Table

from movie_app.db.database import Base

actors_movie = Table("actors_movie", Base.metadata,
                     Column("actor_id", ForeignKey("actors.id"), primary_key=True),
                     Column("movie_id", ForeignKey("movies.id"), primary_key=True))

genre_movie = Table("genre_movie", Base.metadata,
                    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
                    Column("movie_id", ForeignKey("movies.id"), primary_key=True))


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    movies = relationship("Movie", secondary=genre_movie, back_populates="genres")


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    movies = relationship("Movie", secondary=actors_movie, back_populates="actors")


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    premiere = Column(Date)
    description = Column(Text)
    director_id = Column(Integer, ForeignKey("directors.id"))
    genres = relationship("Genre", secondary=genre_movie, back_populates="movies")
    actors = relationship("Actor", secondary=actors_movie, back_populates='movies')
    director = relationship("Director")


