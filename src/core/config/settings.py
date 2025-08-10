from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = Field(..., ge=1, le=65535)
    postgres_db: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", frozen=True)

    @property
    def db_url(self) -> str:
        """Асинхронный DSN для SQLAlchemy (asyncpg)."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sync_db_url(self) -> str:
        """Синхронный DSN для Alembic оффлайн и тестов."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
