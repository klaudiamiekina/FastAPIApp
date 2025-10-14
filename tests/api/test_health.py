import responses
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@responses.activate
def test_health_success():
    responses.add(
        responses.GET,
        "http://openlibrary.org/books/OL1M.json?m=history",
        json={"key": "value"},
        status=200
    )

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["app_status"] == "ok"
    assert data["external_api_status"] == "ok"


@responses.activate
def test_health_failed_status():
    responses.add(
        responses.GET,
        "http://openlibrary.org/books/OL1M.json?m=history",
        status=500
    )

    response = client.get("/health")
    data = response.json()
    assert response.status_code == 200
    assert data["external_api_status"] == "failed"


@responses.activate
def test_health_request_exception():
    responses.add(
        responses.GET,
        "http://openlibrary.org/books/OL1M.json?m=history",
        body=responses.ConnectionError("Timeout")
    )

    response = client.get("/health")
    data = response.json()
    assert response.status_code == 200
    assert data["external_api_status"] == "failed"
