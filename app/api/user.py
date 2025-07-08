"""
User
    GET /users — Получить список всех пользователей.
    POST /users — Создать нового пользователя.
    GET /users/{id} — Получить информацию о пользователе по ID.
    PUT /users/{id} — Обновить информацию о пользователе по ID.
    DELETE /users/{id} — Удалить пользователя по ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.user import UserCRUD
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/user", tags=["user"])
