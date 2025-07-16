from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.crud.order import OrderCRUD
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/order", tags=["order"])


@router.get("/{order_id:int}", response_model=OrderResponse)
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await OrderCRUD.get_by_id(db=db, order_id=order_id)
    return result


@router.get("/by-user_id/{user_id:int}", response_model=OrderResponse)
async def get_last_order_by_user_id(
    user_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderCRUD.get_last_order_by_user_id(db=db, user_id=user_id)
    return result


@router.get("/status/open", response_model=List[OrderResponse])
async def get_all_orders_by_user_id(
    user_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderCRUD.get_open_orders(db=db, user_id=user_id)
    return result


# @router.get("/status/_open", response_model=List[OrderResponse])
# async def get_open_orders(db: AsyncSession = Depends(get_db_session)):
#     """
#     Returns all open orders, without user_id
#     """
#     result = await OrderCRUD._get_open_orders(db=db)
#     return result


@router.get("/status/{status:int}", response_model=List[OrderResponse])
async def get_orders_by_status(
    status: OrderStatus, user_id: int, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderCRUD.get_by_status(db=db, status=status, user_id=user_id)
    return result


# @router.get("/status/_{status:int}", response_model=List[OrderResponse])
# async def get_orders_by_status(status: int, db: AsyncSession = Depends(get_db_session)):
#     """
#     Returns all {status} orders, without user_id
#     """
#     result = await OrderCRUD._get_by_status(db=db, status=status)
#     return result


@router.get("/status/all", response_model=List[OrderResponse])
async def get_orders(user_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await OrderCRUD.get_all(user_id=user_id, db=db)
    return result


# @router.get("/status/_all", response_model=List[OrderResponse])
# async def get_orders(db: AsyncSession = Depends(get_db_session)):
#     """
#     Returns all orders, without user_id
#     """
#     result = await OrderCRUD._get_all(db=db)
#     return result


@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db_session)):
    result = await OrderCRUD.create(db=db, order_create=order)
    return result


@router.put("/{id:int}", response_model=OrderResponse)
async def update_order(
    order_id: int, order_update: OrderUpdate, db: AsyncSession = Depends(get_db_session)
):
    result = await OrderCRUD.update(db=db, order_id=order_id, order_update=order_update)
    return result


@router.delete("/{id:int}", response_model=OrderResponse)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await OrderCRUD.delete(db=db, order_id=order_id)
    return result
