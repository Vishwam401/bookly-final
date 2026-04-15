from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

# Ab hum alag se BASE_DIR calculate nahi karenge, seedha Config wala use karenge
# jo humne Pathlib se robust banaya hai.

mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT, # Config se uthao taaki consistency rahe
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    USE_CREDENTIALS=Config.USE_CREDENTIALS,
    VALIDATE_CERTS=Config.VALIDATE_CERTS,
    # YE SABSE IMPORTANT HAI: Config wala path use karo
    TEMPLATE_FOLDER=Config.TEMPLATE_FOLDER
)

mail = FastMail(
    config=mail_config
)

def create_message(recipient: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipient,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
    return message