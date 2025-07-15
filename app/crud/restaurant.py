from typing import Optional, List, Any, Type, Coroutine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.restaurant import Restaurant
from app.schemas.order import OrderResponse
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)


class RestaurantCRUD:

    @staticmethod
    async def get_all(db: AsyncSession) -> List[RestaurantResponse]:
        result = await db.execute(select(Restaurant))
        restaurants = result.scalars().all()
        return [RestaurantResponse.from_orm(restaurant) for restaurant in restaurants]

    @staticmethod
    async def get_by_id(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
        result = await db.execute(
            select(Restaurant).filter(Restaurant.id == restaurant_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(
        db: AsyncSession, restaurant_name: str
    ) -> List[RestaurantResponse]:
        result = await db.execute(
            select(Restaurant).filter(Restaurant.name == restaurant_name)
        )
        restaurants = result.scalars().all()
        return [RestaurantResponse.from_orm(restaurant) for restaurant in restaurants]

    @staticmethod
    async def create(
        db: AsyncSession, restaurant_create: RestaurantCreate
    ) -> Restaurant:
        """
        Create new restaurant

        Args:
            db: Database AsyncSession
            restaurant_create: Restaurant creation schema

        Returns:
            Restaurant: Created restaurant
        """
        db_restaurant = Restaurant(
            name=restaurant_create.name,
            description=restaurant_create.description,
            street=restaurant_create.street,
            house_number=restaurant_create.house_number,
            apartment=restaurant_create.apartment,
            city=restaurant_create.city,
            country=restaurant_create.country,
        )

        db.add(db_restaurant)
        await db.commit()
        await db.refresh(db_restaurant)

        return db_restaurant

    @staticmethod
    async def update(
        db: AsyncSession, restaurant_id: int, restaurant_update: RestaurantUpdate
    ) -> Optional[Restaurant]:
        """
        Update restaurant

        Args:
            db: Database AsyncSession
            restaurant_id: Restaurant ID
            restaurant_update: Data for update

        Returns:
            Restaurant: Updated Restaurant or None if not found
        """
        db_restaurant = await RestaurantCRUD.get_by_id(db, restaurant_id)
        if not db_restaurant:
            return None

        update_data = restaurant_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_restaurant, field, value)

        await db.commit()
        await db.refresh(db_restaurant)

        return db_restaurant

    @staticmethod
    async def delete(db: AsyncSession, restaurant_id: int):
        """
        Delete restaurant

        Args:
            db: Database AsyncSession
            restaurant_id: Restaurant ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_restaurant = await RestaurantCRUD.get_by_id(db, restaurant_id)
        if not db_restaurant:
            return False

        await db.delete(db_restaurant)
        await db.commit()

        return True
