from unittest.mock import patch

import respx
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from app.clients.open_library_api_client import OpenLibraryAPIClient
import responses
import httpx
import pytest

client = TestClient(app)


def test_fetch_books_by_author_success():
    with respx.mock:
        route = respx.get("https://openlibrary.org/search.json").mock(
            return_value=httpx.Response(200, json={
                "docs": [
                    {
                        "author_name": ["George Orwell"],
                        "ebook_access": "no_ebook",
                        "first_publish_year": 1949,
                        "language": ["eng"],
                        "title": "1984"
                    },
                    {
                        "author_name": ["George Orwell"],
                        "ebook_access": "no_ebook",
                        "first_publish_year": 1945,
                        "language": ["eng"],
                        "title": "Animal Farm"
                    }
                ]
            }
            )
        )

        api_client = OpenLibraryAPIClient()
        result = api_client.fetch_books_by_author("George Orwell")
        titles_from_response = {book["title"] for book in result}
        expected_titles = {"1984", "Animal Farm"}

        assert expected_titles == titles_from_response
        assert route.called


def test_fetch_books_by_author_empty_response():
    responses.add(
        responses.GET,
        "https://openlibrary.org/search.json?author=xyz123",
        json={"docs": []},
        status=200,
    )

    api_client = OpenLibraryAPIClient()
    with pytest.raises(HTTPException) as exc:
        api_client.fetch_books_by_author("xyz123")
    assert exc.value.status_code == 404
    assert "No books found for author 'xyz123'" in exc.value.detail


def test_fetch_books_conn_error(monkeypatch):
    api_client = OpenLibraryAPIClient()

    with patch.object(
            api_client.client, "get", side_effect=httpx.RequestError("Connection error")
    ):
        with pytest.raises(HTTPException) as exc:
            api_client.fetch_books_by_author("Tolkien")

    assert exc.value.status_code == 503
    assert "OpenLibrary unavailable: Connection error" in exc.value.detail


def test_fetch_books_server_error(monkeypatch):
    api_client = OpenLibraryAPIClient()

    with patch.object(
            api_client.client, "get", side_effect=httpx.HTTPStatusError(
                "Server error", request=None, response=type("Response", (), {"status_code": 500})())
    ):
        with pytest.raises(HTTPException) as exc:
            api_client.fetch_books_by_author("Tolkien")

    assert exc.value.status_code == 500
    assert "OpenLibrary API error: Server error" in exc.value.detail
