import logging
from pathlib import Path

from pydantic import BaseModel, ValidationError

from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

from core.config import JSON_STORAGE_FILEPATH

log = logging.getLogger(__name__)


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

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
        log.info("Movie %s created", movie.title)
        self.save_to_file()
        return movie

    def delete_by_slug(self, slug: str) -> None:
        return self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)
        self.save_to_file()

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_to_file()
        return movie

    def partial_update(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_to_file()
        return movie


def create_examples(example_storage: MovieStorage) -> None:
    example_storage.create(
        MovieCreate(
            slug="shawshank",
            title="The Shawshank Redemption",
            description="A banker convicted of uxoricide forms a friendship over a quarter century with a hardened convict,\n"
            " while maintaining his innocence and trying to remain hopeful through simple compassion.",
            year=1994,
        )
    )
    example_storage.create(
        MovieCreate(
            slug="godfather",
            title="The Godfather",
            description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            year=1972,
        )
    )
    example_storage.create(
        MovieCreate(
            slug="batman",
            title="The Dark Knight",
            description="When a menace known as the Joker wreaks havoc and chaos on the people of Gotham,\n"
            " Batman, James Gordon and Harvey Dent must work together to put an end to the madness.",
            year=2008,
        )
    )
    example_storage.save_to_file()


try:
    storage = MovieStorage().load_from_file()
    log.warning("Movie storage loaded from file")
    create_examples(storage)
except ValidationError:
    JSON_STORAGE_FILEPATH.rename("db_corrupted.json")
    storage = MovieStorage()
    log.warning("Movie storage was corrupted, creating a new one")
    create_examples(storage)
