from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db_session
from app.crud.user import UserCRUD
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserChangePassword

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/{id:int}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await UserCRUD.get_by_id(db=db, user_id=user_id)
    return result


@router.get("/by-number/{number}", response_model=UserResponse)
async def get_user_by_number(number: str, db: AsyncSession = Depends(get_db_session)):
    result = await UserCRUD.get_by_number(db=db, number=number)
    return result


@router.get("/by-name/{name}", response_model=UserResponse)
async def get_user_by_name(name: str, db: AsyncSession = Depends(get_db_session)):
    result = await UserCRUD.get_by_name(db=db, name=name)
    return result


@router.post("/", response_model=UserResponse)
async def create_user(
    user_create: UserCreate, db: AsyncSession = Depends(get_db_session)
):
    result = await UserCRUD.create(db=db, user_create=user_create)
    return result


@router.put("/{id:int}", response_model=UserResponse)
async def update_user(
    user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db_session)
):
    result = await UserCRUD.update(db=db, user_id=user_id, user_update=user_update)
    return result


@router.put("/{id:int}/change_password", response_model=UserResponse)
async def change_password(
    user_id: int,
    password_change: UserChangePassword,
    db: AsyncSession = Depends(get_db_session),
):
    result = await UserCRUD.change_password(
        db=db, user_id=user_id, password_change=password_change
    )
    return result


@router.delete("/{id:int}", response_model=UserResponse)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await UserCRUD.delete(db=db, user_id=user_id)
    return result
