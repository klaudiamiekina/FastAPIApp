from typing import Optional, Dict, Union

from sqlalchemy.orm import Session

from app.models.book_model import Books, Authors


class BookDataManager:
    """
    Manages storage and retrieval of books in the local database.

    This class provides methods to:
    - Store books retrieved from an external API, handling duplicates gracefully.
    - Retrieve books from the database, optionally filtered by author and/or title.
    """
    def __init__(self, db: Session):
        self.db = db

    def store_books(self, docs: list[dict]) -> Dict[str, Union[int, str]]:
        """
        Store books in the local database, skipping duplicates based on title+authors.

        Args:
            docs (list[dict]): List of book dictionaries from external API.

        Returns:
            dict: summary with counts of inserted books/authors and duplicates.
        """
        inserted_books = 0
        inserted_authors = 0
        duplicates_count = 0

        for doc in docs:
            title = doc.get("title")
            ebook_access = doc.get("ebook_access")
            first_publish_year = doc.get("first_publish_year")
            language = doc.get("language", "")

            authors_names = doc.get("author_name") or []

            existing_book = (
                self.db.query(Books)
                .join(Books.authors)
                .filter(Books.title == title)
                .filter(Authors.name.in_(authors_names))
                .first()
            )
            if existing_book:
                duplicates_count += 1
                continue

            authors_objs = []
            for name in authors_names:
                author = self.db.query(Authors).filter_by(name=name).first()
                if not author:
                    author = Authors(name=name)
                    self.db.add(author)
                    self.db.flush()
                    inserted_authors += 1
                authors_objs.append(author)

            book = Books(
                title=title,
                ebook_access=ebook_access,
                first_publish_year=first_publish_year,
                language=language,
                authors=authors_objs
            )
            self.db.add(book)
            inserted_books += 1

        self.db.commit()

        message = (
            f"{duplicates_count} book{'s' if duplicates_count != 1 else ''} of requested author already exist in the database"
            if duplicates_count else ""
        )

        return {
            "inserted_books": inserted_books,
            "inserted_authors": inserted_authors,
            "duplicates_count": duplicates_count,
            "message": message
        }

    def get_books(self, author: Optional[str] = None, title: Optional[str] = None):
        """
        Retrieve books from the local database, optionally filtered by author and/or title.
        """
        query = self.db.query(Books)
        if author:
            query = query.join(Books.authors).filter(Authors.name.ilike(f"%{author}%"))
        if title:
            query = query.filter(Books.title.ilike(f"%{title}%"))
        results = query.all()

        for book in results:
            book.authors_list = [author.name for author in book.authors]

        return results
