import pytest
from fastapi.testclient import TestClient
from .main import app


client = TestClient(app)

pytestmark = pytest.mark.api


# def test_today():
#     response = client.get("/today")
#     assert response.status_code == 200
#     assert response.json()


@pytest.fixture
def create_list_item():
    response = client.post(
        "/data", json={"url": "https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"}
    )
    yield response
    # TODO: add removing by id when implemented.


def test_add_content(create_list_item):
    assert create_list_item.status_code == 200
    resp = create_list_item.json()
    assert "id" in resp
    assert resp["id"] > 0
    assert "processed" in resp
    assert resp["processed"] is False
    assert "list" in resp
    assert resp["list"] == "PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"


@pytest.mark.skip
def test_list_content(create_list_item):
    response = client.get("/lists")
    assert response.status_code == 200
    resp = response.json()
    assert isinstance(resp, list)
    assert len(resp) > 0
    for item in resp:
        assert "id" in item, item
        assert item["id"] > 0, item
        assert "processed" in item, item
        assert item["processed"] is False, item
        assert "list" in item, item
        assert item["list"], item
