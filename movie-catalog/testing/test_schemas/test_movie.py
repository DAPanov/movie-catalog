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


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_update_schema(self) -> None:
        movie = Movie(
            title="Movie",
            description="Description",
            year=1999,
            slug="movie",
        )

        movie_update = MovieUpdate(
            title="Movie1",
            description="Description1",
            year=1920,
        )

        for field_name, value in movie_update:
            setattr(movie, field_name, value)

        self.assertEqual(movie_update.title, movie.title)
        self.assertEqual(movie_update.description, movie.description)
        self.assertEqual(movie_update.year, movie.year)
