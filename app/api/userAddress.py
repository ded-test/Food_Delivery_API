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
from typing import Optional, List

from app.core.dependencies import get_db_session
from app.crud.user import UserAddressCRUD
from app.schemas.user import (
    UserAddressCreate,
    UserAddressUpdate,
    UserAddressResponse,
)

router = APIRouter(prefix="/user_address", tags=["user address"])


@router.get("/{id:int}", response_model=UserAddressResponse)
async def get_user_address_by_id(
    user_address_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await UserAddressCRUD.get_by_id(db=db, user_address_id=user_address_id)
    return result


@router.get("/by-user_id/{user_id:int}", response_model=List[UserAddressResponse])
async def get_user_address_by_user_id(
    user_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await UserAddressCRUD.get_by_user_id(db=db, user_id=user_id)
    return result


@router.post("/", response_model=UserAddressResponse)
async def create_user_address(
    user_id: int,
    user_address_create: UserAddressCreate,
    db: AsyncSession = Depends(get_db_session),
):
    result = await UserAddressCRUD.create(
        db=db, user_id=user_id, user_address_create=user_address_create
    )
    return result


@router.put("/{id:int}", response_model=UserAddressResponse)
async def update_user_address(
    user_address_id: int,
    user_address_update: UserAddressUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    result = await UserAddressCRUD.update(
        db=db, user_address_id=user_address_id, user_address_update=user_address_update
    )
    return result


@router.delete("/{id:int}", response_model=UserAddressResponse)
async def delete_user_address(
    user_address_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await UserAddressCRUD.delete(db=db, user_address_id=user_address_id)
    return result
