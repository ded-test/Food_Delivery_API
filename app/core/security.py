from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.core.config import settings
from app.schemas.jwt_token import UserLogin, Token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(
    user_id: int, expires_delta: timedelta, token_type="access"
) -> str:
    to_encode = {
        "sub": str(user_id),
        "type": token_type,
        "exp": int((datetime.utcnow() + expires_delta).timestamp()),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def save_refresh_token(user_id: int, token: str, redis_conn=None):
    token_str = str(token)

    redis_conn.set(
        f"refresh:{user_id}",
        token_str,
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
    )


def get_stored_refresh_token(user_id: int, redis_conn=None) -> str:
    return redis_conn.get(f"refresh:{user_id}")


def remove_refresh_token(user_id: int, redis_conn=None):
    redis_conn.delete(f"refresh:{user_id}")
