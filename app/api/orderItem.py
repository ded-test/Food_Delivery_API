from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.core.dependencies import get_db_session
from app.crud.order import OrderItemCRUD
from app.schemas.order import (
    OrderItemCreate,
    OrderItemUpdate,
    OrderItemResponse,
)

router = APIRouter(prefix="/order_item", tags=["order item"])


@router.get("/{id:int}", response_model=OrderItemResponse)
async def get_order_item_by_id(
    order_item_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderItemCRUD.get_by_id(db=db, order_item_id=order_item_id)
    return result


@router.get("/by-order_id/{order_id:int}", response_model=List[OrderItemResponse])
async def get_order_item_by_order_id(
    order_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderItemCRUD.get_by_order_id(db=db, order_id=order_id)
    return result


@router.post("/", response_model=OrderItemResponse)
async def create_order_item(
    order_item_create: OrderItemCreate, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderItemCRUD.create(db=db, order_item_create=order_item_create)
    return result


@router.put("/{id:int}", response_model=OrderItemResponse)
async def update_iorder_item(
    order_item_id: int,
    item_update: OrderItemUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    result = await OrderItemCRUD.update(
        db=db, order_item_id=order_item_id, item_update=item_update
    )
    return result


@router.delete("/{id:int}", response_model=OrderItemResponse)
async def delete_order_item(
    order_item_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderItemCRUD.delete(db=db, order_item_id=order_item_id)
    return result
