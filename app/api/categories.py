"""
Categories (Category)
    GET /categories — Get a list of all categories.
    POST /categories — Create a new category.
    GET /categories/{id} — Get information about a category by ID.
    PUT /categories/{id} — Update information about a category by ID.
    DELETE /categories/{id} — Delete a category by ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.product import CategoryCRUD
from app.schemas.product import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

router = APIRouter(prefix="/category", tags=["category"])
