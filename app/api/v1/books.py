from fastapi import Query, APIRouter, Depends

from typing import List, Optional

from app.api.descriptions import GET_BOOKS_DESCRIPTION, STORE_BOOKS_DESCRIPTION
from app.dependencies.db import get_db
from app.models.schemas import AuthorRequest, BookResponse, StoreBooksResponse
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("",
             response_model=StoreBooksResponse,
             summary="Fetch books by author and store them in the local database.",
             description=STORE_BOOKS_DESCRIPTION
             )
def fetch_and_store_books(request: AuthorRequest, db=Depends(get_db)):
    service = BookService(db)
    return service.fetch_and_store_books(request.author)


@router.get("",
            response_model=List[BookResponse],
            summary="Retrieve books from the database",
            description=GET_BOOKS_DESCRIPTION)
def get_books(
    author: Optional[str] = Query(None, description="Filter by author name"),
    title: Optional[str] = Query(None, description="Filter by book title"),
    db=Depends(get_db)
):
    service = BookService(db)
    return service.get_books(author=author, title=title)
