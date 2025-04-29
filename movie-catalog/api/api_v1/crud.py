from pydantic import BaseModel

from schemas.movie import Movie, MovieCreate


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        return self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


storage = MovieStorage()


storage.create(
    MovieCreate(
        slug="shawshank",
        title="The Shawshank Redemption",
        description="A banker convicted of uxoricide forms a friendship over a quarter century with a hardened convict,\n"
        " while maintaining his innocence and trying to remain hopeful through simple compassion.",
        year=1994,
    )
)
storage.create(
    MovieCreate(
        slug="godfather",
        title="The Godfather",
        description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        year=1972,
    )
)
storage.create(
    MovieCreate(
        slug="batman",
        title="The Dark Knight",
        description="When a menace known as the Joker wreaks havoc and chaos on the people of Gotham,\n"
        " Batman, James Gordon and Harvey Dent must work together to put an end to the madness.",
        year=2008,
    )
)
