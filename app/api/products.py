"""
Products (Product)
    GET /products — Get a list of all products.
    POST /products — Create a new product.
    GET /products/{id} — Get information about a product by ID.
    PUT /products/{id} — Update information about a product by ID.
    DELETE /products/{id} — Delete a product by ID.
    GET /categories/{category_id}/products — Get a list of products by category.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.product import ProductCRUD
from app.schemas.product import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/products")
async def get_products(db: AsyncSession = Depends(get_db_session)):
    return await ProductCRUD.get_all_products(db)
