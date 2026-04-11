from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config 
from jose import jwt , JWTError

import uuid
import logging


passwd_context = CryptContext(schemes=["argon2"])

ACCESS_TOKEN_EXPIRES = 3600

def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool=False):
    payload = {}
    
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRES)
    )
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    
    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )

        return token_data

    except JWTError as e:
        logging.exception(e)
        return None
