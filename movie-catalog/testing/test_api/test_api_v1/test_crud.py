from os import getenv
from unittest import TestCase

from api.api_v1.crud import storage
from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate

if getenv("TESTING") != "1":
    raise OSError("Environment is not ready for testing")  # noqa: TRY003, EM101


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete_by_slug(self.movie.slug)

    def create_movie(self) -> Movie:
        movie_in = MovieCreate(
            title="title",
            description="description",
            year=1999,
            slug="slug",
        )
        return storage.create(movie_in)

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
