from pathlib import Path

from pydantic import BaseModel, ValidationError

from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_to_file(self):
        db = Path("db.json")
        db.write_text(self.model_dump_json())

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
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


def create_storage() -> MovieStorage:
    example_storage = MovieStorage()
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
    Path("db.json").write_text(example_storage.model_dump_json())
    return example_storage


try:
    storage = MovieStorage().model_validate_json(Path("db.json").read_text())
except ValidationError:
    Path("db.json").rename("db_corrupted.json")
    storage = create_storage()
except FileNotFoundError:
    storage = create_storage()
