import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.crud import storage
from main import app
from schemas.movie import Movie


@pytest.mark.apitest
def test_delete_movie(auth_client: TestClient, movie: Movie) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)
    response = auth_client.delete(url=url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
