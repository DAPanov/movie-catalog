from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.crud import storage
from main import app
from schemas.movie import Movie, MovieUpdate
from testing.conftest import create_movie_random_slug

pytestmark = pytest.mark.apitest


class TestUpdate:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        title, description = request.param
        movie = create_movie_random_slug(title=title, description=description)
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description",
        [
            pytest.param(
                ("some title", "some description"),
                "some title",
                "new description",
                id="same-title-new-description",
            ),
            pytest.param(
                ("another title", "another description"),
                "spam_title",
                "another description",
                id="another-title-same-description",
            ),
            pytest.param(
                ("fizz title", "some description"),
                "",
                "some description",
                id="empty-title-same-description",
            ),
            pytest.param(
                ("fizz title", "some description"),
                "new title",
                "new description",
                id="new-title-new-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movie,
        new_title: str,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_movie", slug=movie.slug)

        update = MovieUpdate(
            title=new_title,
            description=new_description,
            year=datetime.now(tz=UTC).year,
        )
        response = auth_client.put(url, json=update.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(slug=movie.slug)
        assert movie_db
        new_data = MovieUpdate(**movie_db.model_dump())
        assert new_data == update
