from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.crud.product import ProductCRUD
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db_session)):
    result = await ProductCRUD.get_all_products(db)
    return result


@router.get("/{id:int}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await ProductCRUD.get_by_id(db=db, product_id=product_id)
    return result


@router.get("/by-name/{name}", response_model=ProductResponse)
async def get_product_by_name(name: str, db: AsyncSession = Depends(get_db_session)):
    result = await ProductCRUD.get_by_name(db=db, product_name=name)
    return result


@router.get("/category/{category_id:int}", response_model=List[ProductResponse])
async def get_products_by_category(
    category_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await ProductCRUD.get_products_by_category(db=db, category_id=category_id)
    return result


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, db: AsyncSession = Depends(get_db_session)
):
    result = await ProductCRUD.create(db=db, product_create=product)
    return result


@router.put("/{id:int}", response_model=ProductResponse)
async def update_product(
    product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db_session)
):
    result = await ProductCRUD.update(
        db=db, product_id=product_id, product_update=product
    )
    return result


@router.delete("/{id:int}", response_model=ProductResponse)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await ProductCRUD.delete(db=db, product_id=product_id)
    return result
