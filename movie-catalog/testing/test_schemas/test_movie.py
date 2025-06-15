from unittest import TestCase

from schemas.movie import Movie, MovieCreate, MovieUpdate


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_created_schema(self) -> None:
        movie_in = MovieCreate(
            title="Movie",
            description="Description",
            year=1999,
            slug="movie",
        )
        movie = Movie(**movie_in.model_dump())
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.year, movie.year)
        self.assertEqual(movie_in.slug, movie.slug)

    def test_movie_can_be_updated_from_update_schema(self) -> None:
        movie_update = MovieUpdate(
            title="Movie",
            description="Description",
            year=1999,
        )
        movie = Movie(**movie_update.model_dump(), slug="slug")

        self.assertEqual(movie_update.title, movie.title)
        self.assertEqual(movie_update.description, movie.description)
        self.assertEqual(movie_update.year, movie.year)
