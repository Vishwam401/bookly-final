import logging
import uuid
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import Config


passwd_context = CryptContext(schemes=["argon2"])

ACCESS_TOKEN_EXPIRY = 3600  # seconds — 1 hour


def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return passwd_context.verify(password, hashed)


def create_access_token(
    user_data: dict,
    expiry: timedelta = None,
    refresh: bool = False,
) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
    except JWTError as e:
        logging.exception(e)
        return None