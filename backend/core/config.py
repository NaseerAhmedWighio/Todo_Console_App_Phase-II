"""Configuration settings for Todo App backend."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = "sqlite:///./todo_app.db"
    database_url_unpooled: str = "sqlite:///./todo_app.db"
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # PostgreSQL connection parameters
    pghost: str = ""
    pghost_unpooled: str = ""
    pguser: str = ""
    pgdatabase: str = ""
    pgpassword: str = ""

    # Postgres template parameters
    postgres_url: str = ""
    postgres_url_non_pooling: str = ""
    postgres_user: str = ""
    postgres_host: str = ""
    postgres_password: str = ""
    postgres_database: str = ""
    postgres_url_no_ssl: str = ""
    postgres_prisma_url: str = ""

    # JWT settings
    secret_key: str = "your-super-secret-key-change-in-production"
    better_auth_secret: str = "whggm3gaQdfJKdpidboFbLgmnQ2zNIYE"  # Use the same secret as frontend
    access_token_expire_minutes: int = 30

    # Application settings
    app_name: str = "Todo App Backend"
    debug: bool = True
    api_v1_str: str = "/api/v1"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Better Auth integration
    better_auth_secret: Optional[str] = None
    better_auth_url: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()