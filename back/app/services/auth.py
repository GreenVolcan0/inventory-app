from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_ctx.hash(password)

def check_password(plain_password: str, hashed_password: str):
    return pwd_ctx.verify(plain_password, hashed_password)

def _create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expires_at, "type": token_type})
    return jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.JWT_ALG)

def create_access_token(user_id: int, role: str):
    return _create_token(
        {"sub": str(user_id), "role": role},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES),
        token_type="access"
    )

def create_refresh_token(user_id: int):
    return _create_token(
        {"sub": str(user_id)},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRES_DAYS),
        token_type="refresh"
    )

def decode_token(token: str):
    return jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALG])