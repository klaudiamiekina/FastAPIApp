from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    app_name: str = "Library API"
    database_url: str = "postgresql://user_db:password_db@localhost:5432/library_db"
    openlibrary_base_url: str = "https://openlibrary.org"

    model_config = ConfigDict(env_file=".env")

settings = Settings()
