"""
Order items (OrderItem)
    GET /orders/{order_id}/items — Get a list of order items by order ID.
    POST /orders/{order_id}/items — Add an item to an order.
    GET /orders/{order_id}/items/{item_id} — Get information about an order item by ID.
    PUT /orders/{order_id}/items/{item_id} — Update an order item by ID.
    DELETE /orders/{order_id}/items/{item_id} — Delete an order item by ID
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.order import OrderItemCRUD
from app.schemas.order import (
    OrderItemBase,
    OrderItemCreate,
    OrderItemUpdate,
    OrderItemResponse,
)

router = APIRouter(prefix="/order_item", tags=["order item"])
