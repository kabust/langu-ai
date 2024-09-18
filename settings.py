from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LanguAI"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./project.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
