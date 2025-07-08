"""
UserAddress
    GET /users/{user_id}/addresses — Get a list of user addresses.
    POST /users/{user_id}/addresses — Create a new address for a user.
    GET /users/{user_id}/addresses/{address_id} — Get information about an address by ID.
    PUT /users/{user_id}/addresses/{address_id} — Update an address by ID.
    DELETE /users/{user_id}/addresses/{address_id} — Delete an address by ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.user import UserAddressCRUD
from app.schemas.user import (
    UserAddressBase,
    UserAddressCreate,
    UserAddressUpdate,
    UserAddressResponse,
)

router = APIRouter(prefix="/user_address", tags=["user address"])
