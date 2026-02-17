from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ownership.db"
    rate_limit_write: str = "10/minute"
    rate_limit_read: str = "30/minute"
    app_title: str = "Ali-Problemy API"

    model_config = {"env_prefix": "APP_"}


settings = Settings()
