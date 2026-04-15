import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory setup (src folder)
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0" # Render env mein override ho jayega
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str = "localhost:8000"

    # Template path setup jo Linux/Render pe na phate
    TEMPLATE_FOLDER: str = str(BASE_DIR / "templates")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True