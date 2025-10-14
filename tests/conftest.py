import pytest
from unittest.mock import MagicMock
from app.services.book_data_manager import BookDataManager


@pytest.fixture
def mock_db():
    db = MagicMock()
    return db


@pytest.fixture
def book_manager(mock_db):
    return BookDataManager(mock_db)


@pytest.fixture
def sample_books():
    author1 = MagicMock()
    author1.name = "George Orwell"

    author2 = MagicMock()
    author2.name = "Aldous Huxley"

    book1 = MagicMock(title="1984", authors=[author1])
    book2 = MagicMock(title="Animal Farm", authors=[author1])
    book3 = MagicMock(title="Brave New World", authors=[author2])

    return [book1, book2, book3]


def mock_get_books(author=None, title=None):
    books = [
        {"title": "1984", "authors": ["George Orwell"], "ebook_access": "no_ebook",
         "first_publish_year": 1949, "language": ["eng"]},
        {"title": "Animal Farm", "authors": ["George Orwell"], "ebook_access": "no_ebook",
         "first_publish_year": 1945, "language": ["eng"]}
    ]
    result = [
        b for b in books
        if (author is None or author in b["authors"])
        and (title is None or title == b["title"])
    ]
    return result
