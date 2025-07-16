from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db_session
from app.crud.product import CategoryCRUD
from app.schemas.product import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_all_category(db: AsyncSession = Depends(get_db_session)):
    result = await CategoryCRUD.get_all(db=db)
    return result


@router.get("/{id:int}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await CategoryCRUD.get_by_id(db=db, category_id=category_id)
    return result


@router.get("/by-name/{name}", response_model=CategoryResponse)
async def get_category_by_name(
    category_name: str, db: AsyncSession = Depends(get_db_session)
):
    result = await CategoryCRUD.get_by_name(db=db, category_name=category_name)
    return result


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate, db: AsyncSession = Depends(get_db_session)
):
    result = await CategoryCRUD.create(db=db, category_create=category)
    return result


@router.put("/{id:int}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    result = await CategoryCRUD.update(
        db=db, category_id=category_id, category_update=category_update
    )
    return result


@router.delete("/{id:int}", response_model=CategoryResponse)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await CategoryCRUD.delete(db=db, category_id=category_id)
    return result
