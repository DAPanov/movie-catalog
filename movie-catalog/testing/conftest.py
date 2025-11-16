import secrets
from collections.abc import Generator
from os import getenv

import pytest
from _pytest.fixtures import SubRequest

from schemas.movie import Movie, MovieCreate
from storage.movies.crud import storage


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit("Environment is not ready for testing")


def build_movie_create(
    slug: str,
    description: str = "description",
    title: str = "title",
) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        title=title,
        description=description,
        year=1999,
    )


def build_movie_create_random_slug(
    title: str = "title",
    description: str = "description",
) -> MovieCreate:
    slug = secrets.token_hex(7)
    return build_movie_create(
        slug=slug,
        title=title,
        description=description,
    )


def create_movie(
    slug: str,
    title: str = "title",
    description: str = "description",
) -> Movie:
    movie_in = build_movie_create(
        slug=slug,
        title=title,
        description=description,
    )
    return storage.create(movie_in)


def create_movie_random_slug(
    title: str = "title",
    description: str = "description",
) -> Movie:
    movie_in = build_movie_create_random_slug(
        title=title,
        description=description,
    )
    return storage.create(movie_in)


@pytest.fixture(
    params=[
        "slug",
        "foo_slug",
        pytest.param("slg", id="min-slug"),
        pytest.param("another-slug", id="max-slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


@pytest.fixture()
def movie_random_slug() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
