import logging
from pathlib import Path

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

from core.config import JSON_STORAGE_FILEPATH

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES_CATALOG,
    decode_responses=True,
)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_to_file(self) -> None:
        JSON_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Data successfully saved to file")

    @classmethod
    def load_from_file(cls) -> "MovieStorage":
        if not JSON_STORAGE_FILEPATH.exists():
            return MovieStorage()
        return cls.model_validate_json(JSON_STORAGE_FILEPATH.read_text())

    def init_storage_from_file(self) -> None:
        try:
            data = MovieStorage.load_from_file()
        except ValidationError:
            JSON_STORAGE_FILEPATH.rename("db_corrupted.json")
            self.save_to_file()
            log.warning("Movie storage was corrupted, creating a new one")
            return
        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        log.warning("Movie storage loaded from file")

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        redis.hset(
            name=config.REDIS_HASH_MOVIES_CATALOG_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        self.slug_to_movie[movie.slug] = movie
        log.info("Movie %s created", movie.title)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        return self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie

    def partial_update(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        return movie


storage = MovieStorage()
