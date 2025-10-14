from fastapi import FastAPI
from app.api.v1.router import router as api_router

from app.api.v1 import books, health
from app.core.database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Library API",
    description="""
        Library API provides endpoints to fetch books from an external API,
        store them in a local database, and retrieve them with optional filters.
        
        The API supports:
        
        - Fetching and storing books by author
        - Retrieving books with filters by author or title
        - Checking application and external API health
    """,
    version="1.0.0"
)

app.include_router(api_router)
