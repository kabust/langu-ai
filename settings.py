import secrets

from fastapi.templating import Jinja2Templates
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LanguAI"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./project.db"
    TEMPLATES = Jinja2Templates(directory="templates")
    ACCESS_TOKEN_EXPIRE_MS = 7200
    SECRET_KEY = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
