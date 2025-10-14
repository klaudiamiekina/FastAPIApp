import httpx
from fastapi import HTTPException

from app.core.settings import settings

class OpenLibraryAPIClient:
    """
    Client for interacting with the OpenLibrary API.

    This class provides methods to query the OpenLibrary API for books
    and handle HTTP errors gracefully. It uses a persistent `httpx.Client`
    for better performance and connection reuse.
    """
    BASE_URL = settings.openlibrary_base_url

    def __init__(self):
        """Initializes the HTTP client with a base URL and a default timeout."""
        self.client = httpx.Client(base_url=self.BASE_URL, timeout=5.0)

    def fetch_books_by_author(self, author_name: str):
        """
        Fetches books from the OpenLibrary API by a given author's name.

        Sends a GET request to the `/search.json` endpoint with the `author` parameter
        and returns a list of matching book records from the API response.

        Args:
            author_name (str): Name of the author whose books should be fetched.

        Returns:
            list[dict]: A list of book objects (each represented as a dictionary)
            returned by the OpenLibrary API.

        Raises:
            HTTPException:
                - 503 if the OpenLibrary service is unavailable or the request fails.
                - With the corresponding status code if the API returns an HTTP error.
        """
        try:
            response = self.client.get(
                "/search.json",
                params={"author": author_name}
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("docs"):
                raise HTTPException(status_code=404, detail=f"No books found for author '{author_name}'")
            return data.get("docs", [])

        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"OpenLibrary unavailable: {e}")

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"OpenLibrary API error: {e}")
