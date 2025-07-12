from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db_session
from app.crud.restaurant import RestaurantCRUD
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

@router.get("/", response_model=RestaurantResponse)
async def get_all_restaurants(db: AsyncSession = Depends(get_db_session)):
    result = await RestaurantCRUD.get_all(db=db)
    return result

@router.get("/{id:int}", response_model=RestaurantResponse)
async def get_restaurant_by_id(restaurant_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await RestaurantCRUD.get_by_id(db=db, restaurant_id=restaurant_id)
    return result

@router.get("/by-name/{name:str}", response_model=RestaurantResponse)
async def get_restaurant_by_name(restaurant_name: str, db: AsyncSession = Depends(get_db_session)):
    result = await RestaurantCRUD.get_by_name(db=db, restaurant_name=restaurant_name)
    return result

@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(restaurant_create: RestaurantCreate, db: AsyncSession = Depends(get_db_session)):
    result = await RestaurantCRUD.create(db=db, restaurant_create=restaurant_create)
    return result

@router.put("/{id:int}", response_model=RestaurantResponse)
async def update_restaurant(restaurant_id: int, restaurant_update: RestaurantUpdate, db: AsyncSession = Depends(get_db_session)):
    result = await RestaurantCRUD.update(db=db, restaurant_id=restaurant_id, restaurant_update=restaurant_update)
    return result

@router.delete("/{id:int}", response_model=RestaurantResponse)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await RestaurantCRUD.delete(db=db, restaurant_id=restaurant_id)
    return result