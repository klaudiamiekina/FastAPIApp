from sqlalchemy import Column, Integer, String, Table, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column(
        "book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True
    )
)

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    ebook_access = Column(String)
    first_publish_year = Column(Integer)
    language = Column(ARRAY(String), nullable=False, default=list)

    authors = relationship(
        "Authors",
        secondary=book_authors,
        back_populates="books"
    )

class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship(
        "Books",
        secondary=book_authors,
        back_populates="authors"
    )
