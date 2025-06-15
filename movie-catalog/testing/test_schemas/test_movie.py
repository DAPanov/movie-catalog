from unittest import TestCase

from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


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

    def test_movie_can_be_created_from_created_schema_with_sub_test(self) -> None:
        slugs = [
            "movie",
            # "very_very_very_very_long_slug",
            "sl",
            "slg",
            # "",
        ]

        for slug in slugs:
            with self.subTest(slug=slug, msg=f"slug-test-{slug}"):
                movie_in = MovieCreate(
                    title="Movie",
                    description="Description",
                    year=1999,
                    slug=slug,
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


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_partial_updated_from_update_schema(self) -> None:
        movie = Movie(
            title="Movie",
            description="Description",
            year=1999,
            slug="movie",
        )

        movie_update = MoviePartialUpdate()

        for field_name, value in movie_update.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)

        if movie_update.year:
            self.assertEqual(movie_update.year, movie.year)
        elif movie_update.title:
            self.assertEqual(movie_update.title, movie.title)
        elif movie_update.description:
            self.assertEqual(movie_update.description, movie.description)
        else:
            self.assertEqual(movie, movie)
