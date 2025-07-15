from datetime import timedelta
import redis

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_redis, get_db_session

from app.core.security import (
    verify_password,
    create_token,
    save_refresh_token,
    get_stored_refresh_token,
    remove_refresh_token,
    oauth2_scheme,
)
from app.crud.user import UserCRUD
from app.schemas.jwt_token import Token, UserLogin
from app.core.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db_session),
    db_redis: redis.Redis = Depends(get_redis),
):
    db_user = await UserCRUD.authenticate(db, data.number, data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token(
        db_user.id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        db_user.id,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )

    await save_refresh_token(db_user.id, refresh_token, db_redis)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db_redis: redis.Redis = Depends(get_redis)):
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Wrong token type")
        user_id = int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    stored = await get_stored_refresh_token(user_id, db_redis)
    if stored != refresh_token:
        raise HTTPException(status_code=401, detail="Revoked token")

    access = await create_token(
        user_id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access, refresh_token=refresh_token)


@router.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return {"user_id": payload["sub"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme), db_redis: redis.Redis = Depends(get_redis)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    await remove_refresh_token(user_id, db_redis)
    return {"detail": "Logged out"}
