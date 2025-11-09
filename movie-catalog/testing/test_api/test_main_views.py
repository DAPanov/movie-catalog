import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.apitest


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = "Hello World"
    assert response_data["message"] == expected_message, response_data


@pytest.mark.parametrize("name", ["John", "", "foo bar", "1213!@#"])
def test_root_view_custom_name(client: TestClient, name: str) -> None:
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = f"Hello {name}"
    assert response_data["message"] == expected_message, response_data
