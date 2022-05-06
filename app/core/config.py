"""Settings."""
from typing import Any

from pydantic import BaseSettings, validator
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):

    API_PREFIX: str = "/api"

    POSTGRES_USER: str = "root"
    POSTGRES_PASSWORD: str = "root"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "dev"
    SQLALCHEMY_DATABASE_URI: str | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: str | None, values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        postgres_db = {
            "drivername": "postgresql",
            "username": values.get("POSTGRES_USER"),
            "password": values.get("POSTGRES_PASSWORD"),
            "host": values.get("POSTGRES_HOST"),
            "port": values.get("POSTGRES_PORT"),
            "database": values.get("POSTGRES_DB")
        }
        return str(URL.create(**postgres_db))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
