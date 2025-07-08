"""
Restaurants (Restaurant)
    GET /restaurants — Get a list of all restaurants.
    POST /restaurants — Create a new restaurant.
    GET /restaurants/{id} — Get information about a restaurant by ID.
    PUT /restaurants/{id} — Update information about a restaurant by ID.
    DELETE /restaurants/{id} — Delete a restaurant by ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import DatabaseManager, RedisManager, get_redis, get_db_session
from app.crud.restaurant import RestaurantCRUD
from app.schemas.restaurant import (
    RestaurantBase,
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)

router = APIRouter(prefix="/restaurant", tags=["restaurant"])
