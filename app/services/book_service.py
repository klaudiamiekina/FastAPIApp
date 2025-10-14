import requests

from fastapi import HTTPException, status

from app.clients.open_library_api_client import OpenLibraryAPIClient
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.schemas import StoreBooksResponse, BookResponse
from app.services.book_data_manager import BookDataManager


class BookService:
    """
    Service layer responsible for fetching books from an external API
    and interacting with the database via BookDataManager.
    """
    def __init__(self, db: Session):
        """
        Initialize the BookService with a database session.

        Args:
            db (Session): SQLAlchemy session connected to the database.
        """
        self.book_data_manager = BookDataManager(db)
        self.client = OpenLibraryAPIClient()

    def fetch_and_store_books(self, author_name: str) -> StoreBooksResponse:
        """
        Fetch books by author from OpenLibrary API and store them in the database.

        Args:
            author_name (str): Name of the author to fetch books for.

        Returns:
            StoreBooksResponse: Pydantic model containing summary of inserted books,
            inserted authors, duplicates count, and optional message.

        Raises:
            HTTPException: If fetching from OpenLibrary fails.
        """
        try:
            docs = self.client.fetch_books_by_author(author_name)
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to fetch books from OpenLibrary: {str(e)}"
            )
        result = self.book_data_manager.store_books(docs)
        return StoreBooksResponse(**result)

    def get_books(self, author: Optional[str] = None, title: Optional[str] = None) -> List[BookResponse]:
        """
        Retrieve books from the database, optionally filtered by author and/or title.

        Args:
            author (Optional[str]): Filter books by author name (partial match).
            title (Optional[str]): Filter books by title (partial match).

        Returns:
            List[BookResponse]: List of books validated and serialized as Pydantic models.
        """
        books = self.book_data_manager.get_books(author, title)
        response = [
            BookResponse(
                title=book.title,
                ebook_access=book.ebook_access,
                first_publish_year=book.first_publish_year,
                authors=book.authors_list,
                language=book.language
            )
            for book in books
        ]
        return response
