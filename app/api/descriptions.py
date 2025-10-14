STORE_BOOKS_DESCRIPTION = """
    Fetches books from an external API by author name and stores them in the local database.
    \nThe response includes:
    \n- `inserted_books`: number of books successfully stored
    \n- `inserted_authors`: number of authors successfully stored
    \n- `duplicates_count`: number of books/authors that already exist in the database
    \n- `message`: summary message describing the result or any error encountered
"""

GET_BOOKS_DESCRIPTION = """
    Returns a list of books from the local database.
    \nYou can optionally filter the results by author and/or title.
    \nEach book in the response includes:
    \n- `title`: title of the book
    \n- `ebook_access`: access type of ebook, if available
    \n- `first_publish_year`: year the book was first published
    \n- `authors`: list of authors
    \n- `language`: list of languages the book is available in
"""

HEALTH_DESCRIPTION = """
    Checks the health of the application and the external API. 
    \nThe response includes:
    \n- `app_status`: status of the application itself
    \n- `external_api_status`: status of the connection to the external API
"""