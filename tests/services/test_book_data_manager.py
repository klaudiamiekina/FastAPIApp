import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock

client = TestClient(app)


def test_store_books_counts(book_manager, mock_db):
    books = [
        {"title": "1984", "author_name": ["George Orwell"], "ebook_access": "no_ebook",
         "first_publish_year": 1949, "language": ["eng"]},
        {"title": "Brave New World", "author_name": ["Aldous Huxley"], "ebook_access": "no_ebook",
         "first_publish_year": 1932, "language": ["eng"]},
    ]

    mock_query = MagicMock()
    mock_query.join.return_value.filter.return_value.filter.return_value.first.side_effect = [
        None, None, MagicMock(), MagicMock()
    ]
    mock_db.query.return_value = mock_query

    result = book_manager.store_books(books)
    assert result["inserted_books"] == 2
    assert result["duplicates_count"] == 0

    result2 = book_manager.store_books(books)
    assert result2["inserted_books"] == 0
    assert result2["duplicates_count"] == 2
    assert "2 books of requested author already exist in the database" in result2["message"]


def test_store_books_empty_list(book_manager, mock_db):
    result = book_manager.store_books([])
    assert result == {
        "inserted_books": 0,
        "inserted_authors": 0,
        "duplicates_count": 0,
        "message": ""
    }


def test_store_books_single_duplicate(book_manager, mock_db):
    books = {
        "title": "The Hobbit",
        "author_name": ["J.R.R. Tolkien"],
        "ebook_access": "no_ebook",
        "first_publish_year": 1937,
        "language": ["eng"]
    }

    mock_books_query = MagicMock()
    mock_books_query.join.return_value.filter.return_value.filter.return_value.first.return_value = MagicMock()
    mock_authors_query = MagicMock()
    mock_authors_query.filter_by.return_value.first.return_value = None
    mock_db.query = MagicMock(side_effect=[mock_books_query, mock_authors_query])

    result = book_manager.store_books([books])

    assert result["inserted_books"] == 0
    assert result["inserted_authors"] == 0
    assert result["duplicates_count"] == 1
    assert result["message"] == "1 book of requested author already exist in the database"


def test_get_books_no_filter(book_manager, mock_db, sample_books):
    books = sample_books[:2]

    mock_query = MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = books
    mock_db.query.return_value = mock_query

    result = book_manager.get_books()

    assert len(result) == 2
    titles = [book.title for book in result]
    assert titles == ["1984", "Animal Farm"]

    for book in result:
        assert hasattr(book, "authors_list")
        assert book.authors_list == ["George Orwell"]


def test_get_books_filter_author(book_manager, mock_db, sample_books):
    books = sample_books

    mock_query = MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.side_effect = lambda: [book for book in books if
                                          any(a.name == "George Orwell" for a in book.authors)]
    mock_db.query.return_value = mock_query

    result = book_manager.get_books(author="George Orwell")

    filtered_titles = [book.title for book in result]
    assert filtered_titles == ["1984", "Animal Farm"]

    for book in result:
        assert hasattr(book, "authors_list")
        assert "George Orwell" in book.authors_list


def test_get_books_filter_title(book_manager, mock_db, sample_books):
    books = sample_books

    mock_query = MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query

    mock_query.all.side_effect = lambda: [
        book for book in books if "1984" in book.title
    ]

    mock_db.query.return_value = mock_query

    result = book_manager.get_books(title="1984")

    filtered_titles = [book.title for book in result]
    assert filtered_titles == ["1984"]

    for book in result:
        assert hasattr(book, "authors_list")
        assert any(isinstance(name, str) for name in book.authors_list)


def test_get_books_filter_author_and_title(book_manager, mock_db, sample_books):
    books = sample_books

    mock_query = MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query

    mock_query.all.side_effect = [
        [book for book in books if book.title == "1984" and any(a.name == "George Orwell" for a in book.authors)],
        []
    ]

    mock_db.query.return_value = mock_query

    result1 = book_manager.get_books(author="George Orwell", title="1984")
    filtered_titles = [book.title for book in result1]
    assert filtered_titles == ["1984"]

    result2 = book_manager.get_books(author="George Orwell", title="Brave New World")
    assert result2 == []
