import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

pytestmark = pytest.mark.api


# def test_today():
#     response = client.get("/today")
#     assert response.status_code == 200
#     assert response.json()


def test_add_content():
    response = client.post(
        "/data", json={"url": "https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"}
    )
    assert response.status_code == 200
    resp = response.json()
    assert "id" in resp
    assert resp["id"] > 0
    assert "processed" in resp
    assert resp["processed"] is False
    assert "list" in resp
    assert resp["list"] == "PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK"
