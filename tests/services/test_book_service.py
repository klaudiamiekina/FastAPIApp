import pytest
import requests
from fastapi import HTTPException
from unittest.mock import Mock, patch

from app.services.book_service import BookService
from app.models.schemas import StoreBooksResponse, BookResponse


def test_fetch_and_store_books_success(mock_db):
    mock_docs = [
        {"title": "The Hobbit", "author_name": ["J.R.R. Tolkien"],
         "first_publish_year": 1937, "language": ["en"], "ebook_access": "no_ebook"},
        {"title": "The Fellowship of the Ring", "author_name": ["J.R.R. Tolkien"],
         "first_publish_year": 1954, "language": ["en"], "ebook_access": "available"},
    ]
    mock_store_result = {
        "inserted_books": 2,
        "inserted_authors": 1,
        "duplicates_count": 0,
        "message": ""
    }
    with patch("app.clients.open_library_api_client.OpenLibraryAPIClient.fetch_books_by_author",
               return_value=mock_docs):
        with patch("app.services.book_data_manager.BookDataManager.store_books",
                   return_value=mock_store_result):
            service = BookService(db=mock_db)
            response = service.fetch_and_store_books("J.R.R. Tolkien")

    assert isinstance(response, StoreBooksResponse)
    assert response.inserted_books == 2
    assert response.inserted_authors == 1
    assert response.duplicates_count == 0


def test_fetch_and_store_books_api_failure(mock_db):
    with patch(
            "app.clients.open_library_api_client.OpenLibraryAPIClient.fetch_books_by_author",
            side_effect=requests.exceptions.RequestException("API down")
    ):
        service = BookService(db=mock_db)

        with pytest.raises(HTTPException) as exc_info:
            service.fetch_and_store_books("J.K. Rowling")

    assert exc_info.value.status_code == 502
    assert "Failed to fetch books from OpenLibrary: API down" in exc_info.value.detail


def test_get_books_returns_list(mock_db):
    mock_books = [
        Mock(
            title="1984",
            ebook_access="no_ebook",
            first_publish_year=1949,
            authors_list=["George Orwell"],
            language=["en"]
        ),
        Mock(
            title="Animal Farm",
            ebook_access="available",
            first_publish_year=1945,
            authors_list=["George Orwell"],
            language=["en"]
        )
    ]

    with patch("app.services.book_data_manager.BookDataManager.get_books", return_value=mock_books):
        service = BookService(db=mock_db)
        result = service.get_books(author="George Orwell")

    assert isinstance(result, list)
    assert all(isinstance(b, BookResponse) for b in result)
    assert result[0].title == "1984"
    assert result[1].title == "Animal Farm"


def test_get_books_passes_filters(mock_db):
    with patch("app.services.book_data_manager.BookDataManager.get_books") as mock_get_books:
        mock_get_books.return_value = []

        service = BookService(db=mock_db)
        service.get_books(author="J.K. Rowling", title="Harry Potter and the Sorcerer's Stone")

        mock_get_books.assert_called_once_with("J.K. Rowling", "Harry Potter and the Sorcerer's Stone")
