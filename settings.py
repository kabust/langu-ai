from fastapi.templating import Jinja2Templates
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LanguAI"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./project.db"
    TEMPLATES = Jinja2Templates(directory="templates")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
