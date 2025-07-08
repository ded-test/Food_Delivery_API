"""
Orders (Order)
    GET /orders — Get a list of all orders.
    POST /orders — Create a new order.
    GET /orders/{id} — Get information about an order by ID.
    PUT /orders/{id} — Update information about an order by ID.
    DELETE /orders/{id} — Delete an order by ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.order import OrderCRUD
from app.schemas.order import OrderBase, OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/order", tags=["order"])
