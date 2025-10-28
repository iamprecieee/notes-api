from datetime import datetime, timedelta, timezone
import hashlib
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    return pwd_context.hash(password_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")

    return pwd_context.verify(password_bytes, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    settings = get_settings()

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expiry
    )
    to_encode.update({"exp": expire})

    hashed_key = hashlib.sha256(settings.secret_key.encode("utf-8")).hexdigest()

    encoded_jwt = jwt.encode(
        to_encode,
        hashed_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    settings = get_settings()

    hashed_key = hashlib.sha256(settings.secret_key.encode("utf-8")).hexdigest()

    payload = jwt.decode(
        token,
        hashed_key,
        algorithms=[settings.algorithm],
    )
    return payload
