from typing import Optional, List

from pydantic import BaseModel, Field


class AuthorRequest(BaseModel):
    author: str = Field(
        ...,
        min_length=1,
        description="Name of the author to fetch books for",
        json_schema_extra={"example": "J.R.R. Tolkien"}
    )


class BookResponse(BaseModel):
    title: str = Field(
        ...,
        description="Title of the book",
        json_schema_extra={"example": "The Lord of the Rings"}
    )
    ebook_access: Optional[str] = Field(
        None,
        description="Access type of ebook, if available",
        json_schema_extra={"example": "no_ebook"}
    )
    first_publish_year: Optional[int] = Field(
        None,
        description="Year the book was first published",
        json_schema_extra={"example": 1997}
    )
    authors: List[str] = Field(
        default_factory=list,
        description="List of authors",
        json_schema_extra={"example": ["J.R.R. Tolkien"]}

    )
    language: List[str] = Field(
        default_factory=list,
        description="List of languages the book is available in",
        json_schema_extra={"example": ["en", "pl"]}
    )

    model_config = {
        "from_attributes": True
    }


class StoreBooksResponse(BaseModel):
    inserted_books: int = Field(
        ...,
        description="Number of new books inserted into the database",
        json_schema_extra={"example": 5}
    )
    inserted_authors: int = Field(
        ...,
        description="Number of new authors inserted",
        json_schema_extra={"example": 2}
    )
    duplicates_count: int = Field(
        ...,
        description="Number of books/authors already existing in the database",
        json_schema_extra={"example": 50}
    )
    message: str = Field(
        ...,
        description="Summary message for the operation",
        json_schema_extra={"example": "50 books of requested author already exist in the database"}
    )


class HealthResponse(BaseModel):
    app_status: str = Field(
        ...,
        description="Status of the application",
        json_schema_extra={"example": "ok"}
    )
    external_api_status: str = Field(
        ...,
        description="Status of external API connection",
        json_schema_extra={"example": "failed"}
    )
