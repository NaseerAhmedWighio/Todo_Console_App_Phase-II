from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and configuration management.
    """

    app_name: str = "Todo App Console"
    app_version: str = "0.1.0"
    debug: bool = False

    # In-memory storage limits
    max_tasks: int = 1000

    # API settings
    api_prefix: str = "/api/v1"
    allowed_origins: str = "*"  # Comma-separated list of allowed origins

    # Logging
    log_level: str = "INFO"

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000

    # Database settings
    db_path: str = "todo_app.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a global settings instance
settings = Settings()


def get_allowed_origins():
    """Parse the allowed_origins string into a list."""
    if settings.allowed_origins == "*":
        return ["*"]
    return [
        origin.strip()
        for origin in settings.allowed_origins.split(",")
        if origin.strip()
    ]
