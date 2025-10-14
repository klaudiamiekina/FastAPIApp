from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

from app.services.book_service import BookService
from tests.conftest import mock_get_books

client = TestClient(app)


def test_fetch_and_store_books_success(mock_db):
    mock_result = {"inserted_books": 1, "inserted_authors": 1, "duplicates_count": 0, "message": ""}

    with patch.object(BookService, 'fetch_and_store_books', return_value=mock_result) as mock_service:
        response = client.post("/books", json={"author": "J.R.R. Tolkien"})
        assert response.status_code == 200
        assert response.json() == mock_result

        mock_service.assert_called_once_with("J.R.R. Tolkien")


def test_fetch_and_store_books_service_error(mock_db):
    with patch.object(BookService, "fetch_and_store_books", side_effect=HTTPException(status_code=502)):
        response = client.post("/books", json={"author": "George Orwell"})
        assert response.status_code == 502


def test_fetch_and_store_books_invalid_request_simple():
    response = client.post("/books", json={"author": ""})
    assert response.status_code == 422


def test_get_books_no_filters(mock_db):
    fake_books = [
        {
            "title": "1984",
            "authors": ["George Orwell"],
            "ebook_access": "no_ebook",
            "first_publish_year": 1949,
            "language": ["eng"]
        }
    ]
    with patch.object(BookService, "get_books", return_value=fake_books) as mock_service:
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json() == fake_books
        mock_service.assert_called_once_with(author=None, title=None)


def test_get_books_with_author_filter(mock_db):
    fake_books = [
        {
            "title": "Brave New World",
            "authors": ["Aldous Huxley"],
            "ebook_access": "no_ebook",
            "first_publish_year": 1932,
            "language": ["eng"]
        }
    ]
    with patch.object(BookService, "get_books", return_value=fake_books) as mock_service:
        response = client.get("/books", params={"author": "Aldous Huxley"})
        assert response.status_code == 200
        assert response.json() == fake_books
        mock_service.assert_called_once_with(author="Aldous Huxley", title=None)


def test_get_books_with_title_filter(mock_db):
    fake_books = [
        {
            "title": "The Hobbit",
            "authors": ["J.R.R. Tolkien"],
            "ebook_access": "no_ebook",
            "first_publish_year": 1937,
            "language": ["eng"]
        }
    ]
    with patch.object(BookService, "get_books", return_value=fake_books) as mock_service:
        response = client.get("/books", params={"title": "The Hobbit"})
        assert response.status_code == 200
        assert response.json() == fake_books
        mock_service.assert_called_once_with(author=None, title="The Hobbit")


def test_get_books_with_author_and_title_filter(mock_db):
    fake_books = [
        {
            "title": "1984",
            "authors": ["George Orwell"],
            "ebook_access": "no_ebook",
            "first_publish_year": 1949,
            "language": ["eng"]
        }
    ]

    with patch.object(BookService, "get_books", return_value=fake_books) as mock_service:
        response = client.get("/books", params={"author": "George Orwell", "title": "1984"})

        assert response.status_code == 200
        assert response.json() == fake_books
        mock_service.assert_called_once_with(author="George Orwell", title="1984")


def test_get_books_with_author_and_mismatch_title_filter(mock_db):
    with patch.object(BookService, "get_books", side_effect=mock_get_books) as mock_service:
        response = client.get("/books", params={"author": "George Orwell", "title": "xyz"})
        assert response.status_code == 200
        assert response.json() == []

        mock_service.assert_called_once_with(author="George Orwell", title="xyz")
