import pytest
import schemathesis
from fastapi.testclient import TestClient

from .main import app

# Globally enable OpenAPI 3.1 experimental feature
schemathesis.experimental.OPEN_API_3_1.enable()


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
    assert create_list_item.status_code == 200, create_list_item.text
    resp = create_list_item.json()
    assert "id" in resp
    assert resp["id"] > 0
    assert "processed" in resp
    assert resp["processed"] is False
    assert "list" in resp
    assert resp["list"] == "PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"


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


schema = schemathesis.from_uri(
    "http://127.0.0.1:8000/openapi.json",
)


@pytest.mark.auto_generated
@schema.parametrize()
def test_api(case):
    case.call_and_validate()
