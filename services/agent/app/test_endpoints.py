import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

pytestmark = pytest.mark.api


@pytest.fixture
def create_list_item():
    response = client.post(
        "/data", json={"url": "https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"}
    )
    yield response
    # TODO: add removing by id when implemented.


def test_add_content(create_list_item):
    assert create_list_item.status_code == 200, create_list_item.text
    resp = create_list_item.json()
    assert "id" in resp
    assert resp["id"] > 0
    assert "processed" in resp
    assert resp["processed"] is False
    assert "list" in resp
    assert resp["list"] == "PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"


def test_add_content_duplicates():
    response_initial = client.post(
        "/data", json={"url": "https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZL"}
    )
    assert response_initial.status_code == 200, response_initial.text
    resp = response_initial.json()
    assert "id" in resp
    assert resp["id"] > 0
    initial_id = resp["id"]
    assert "processed" in resp
    assert resp["processed"] is False
    assert "list" in resp
    assert resp["list"] == "PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZL"

    response_duplicate = client.post(
        "/data", json={"url": "https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZL"}
    )
    assert response_duplicate.status_code == 200, response_duplicate.text
    assert response_duplicate.json()["id"] == initial_id


def test_non_youtube_playlist():
    response = client.post(
        "/data", json={"url": "https://example.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZR"}
    )
    assert response.status_code == 400, response.text


@pytest.mark.parametrize("skip,limit", [(0, 10), (1, 1), (0, 1)])
def test_list_content(create_list_item, skip, limit):
    response = client.get("/lists", params={"skip": skip, "limit": limit})
    assert response.status_code == 200
    resp = response.json()
    assert isinstance(resp, list)
    assert 0 < len(resp) <= limit
    for item in resp:
        assert "id" in item, item
        assert item["id"] > 0, item
        assert "processed" in item, item
        assert item["processed"] is False, item
        assert "list" in item, item
        assert item["list"], item


@pytest.mark.parametrize("skip,limit", [(-1, 10), (10, -1), (9999, 101)])
def test_list_content_negative(create_list_item, skip, limit):
    response = client.get("/lists", params={"skip": skip, "limit": limit})
    assert response.status_code == 422
