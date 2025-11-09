import logging
import secrets
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movie import Movie, MovieCreate
from testing.conftest import build_movie_create_random_slug

pytestmark = pytest.mark.apitest


def test_create_movie(
    caplog: pytest.LogCaptureFixture,
    auth_client: TestClient,
) -> None:
    caplog.set_level(logging.INFO)
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(
        title="title",
        description="description",
        year=1999,
        slug=secrets.token_hex(7),
    )
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = MovieCreate(**response_data)
    assert received_values == movie_create, response_data
    assert "Movie" in caplog.text
    assert movie_create.title in caplog.text


def test_create_movie_already_exists(auth_client: TestClient, movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    data: dict[str, str] = movie_create.model_dump(mode="json")
    url = app.url_path_for("create_movie")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie with slug={movie.slug!r} already exists."
    assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("fo", "string_too_short"), id="Too short slug"),
            pytest.param(
                ("foobarfizzbuzzspamandeggs!", "string_too_long"),
                id="Too long slug",
            ),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(
        self,
        movie_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_movie")
        create_data, expected_error_type = movie_create_values
        response = auth_client.post(url=url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_error_type, error_detail
