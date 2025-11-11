__all__ = (
    "MovieAlreadyExistsError",
    "storage",
)

import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES_CATALOG,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for Movie CRUD actions.
    """


class MovieAlreadyExistsError(Exception):
    """
    Raised on movie creation if such slug already exists.
    """


class MovieStorage(BaseModel):

    def get(self) -> list[Movie]:
        data = redis.hvals(config.REDIS_HASH_MOVIES_CATALOG_NAME)
        return [Movie.model_validate_json(movie) for movie in data]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(
            name=config.REDIS_HASH_MOVIES_CATALOG_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(data)
        return None

    def set_movie_attr(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_HASH_MOVIES_CATALOG_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=config.REDIS_HASH_MOVIES_CATALOG_NAME,
                key=slug,
            ),
        )

    def create_or_raise_if_exists(self, movie_in: MovieCreate) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in)
        raise MovieAlreadyExistsError(movie_in.slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.set_movie_attr(movie)
        log.info("Movie %s created", movie.title)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(config.REDIS_HASH_MOVIES_CATALOG_NAME, slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.set_movie_attr(movie)
        return movie

    def partial_update(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.set_movie_attr(movie)
        return movie


storage = MovieStorage()
