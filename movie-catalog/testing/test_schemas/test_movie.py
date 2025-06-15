from unittest import TestCase

from schemas.movie import Movie, MovieCreate


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
