import secrets
from typing import ClassVar
from unittest import TestCase

from api.api_v1.crud import storage
from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


def create_movie() -> Movie:
    movie_in = MovieCreate(
        title="title",
        description="description",
        year=1999,
        slug=secrets.token_hex(7),
    )

    return storage.create(movie_in)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def tearDown(self) -> None:
        storage.delete_by_slug(self.movie.slug)

    def test_update_movie(self) -> None:
        movie_update = MovieUpdate(**self.movie.model_dump())
        source_description = self.movie.description
        movie_update.description *= 2
        updated_movie = storage.update(movie=self.movie, movie_in=movie_update)
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )

        self.assertEqual(
            movie_update,
            MovieUpdate(**updated_movie.model_dump()),
        )

    def test_partial_update_movie(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description=self.movie.description * 2,
        )
        source_description = self.movie.description
        updated_movie = storage.partial_update(
            movie=self.movie,
            movie_in=movie_partial_update,
        )

        self.assertNotEqual(source_description, updated_movie.description)
        self.assertEqual(
            movie_partial_update.description,
            updated_movie.description,
        )


class MovieStorageGetMovieTestCase(TestCase):
    SHORT_MOVIE_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.SHORT_MOVIE_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        expected_slugs = {mov.slug for mov in self.movies}
        slugs = {mov.slug for mov in movies}
        expected_diff = set()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(movie=movie, msg=f"Validate can get slug {movie.slug!r}"):
                db_movie = storage.get_by_slug(slug=movie.slug)
                self.assertEqual(movie.slug, db_movie.slug)
