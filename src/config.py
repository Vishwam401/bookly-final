import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory setup
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0"
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

    # Placeholder
    TEMPLATE_FOLDER: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()

# --- Path Correction Logic ---
# Pehle check karo current folder (src) mein templates hai?
path_option_1 = BASE_DIR / "templates"
# Phir check karo ek level upar templates hai?
path_option_2 = BASE_DIR.parent / "templates"

if path_option_1.exists() and path_option_1.is_dir():
    Config.TEMPLATE_FOLDER = str(path_option_1)
elif path_option_2.exists() and path_option_2.is_dir():
    Config.TEMPLATE_FOLDER = str(path_option_2)
else:
    # Agar dono nahi mile (Render issue), toh current working directory se try karo
    Config.TEMPLATE_FOLDER = os.path.join(os.getcwd(), "src", "templates")

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True