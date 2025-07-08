from typing import Optional, List, Any, Type
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantCRUD:

    @staticmethod
    def get_by_id(db: Session, restaurant_id: int) -> Optional[Restaurant]:
        return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    @staticmethod
    def get_by_name(db: Session, restaurant_name: str) -> list[Type[Restaurant]]:
        return db.query(Restaurant).filter(Restaurant.name == restaurant_name).all()

    @staticmethod
    def create(db: Session, restaurant_create: RestaurantCreate) -> Restaurant:
        """
        Create new restaurant

        Args:
            db: Database session
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
        db.commit()
        db.refresh(db_restaurant)

        return db_restaurant

    @staticmethod
    def update(
        db: Session, restaurant_id: int, restaurant_update: RestaurantUpdate
    ) -> Optional[Restaurant]:
        """
        Update restaurant

        Args:
            db: Database session
            restaurant_id: Restaurant ID
            restaurant_update: Data for update

        Returns:
            Restaurant: Updated Restaurant or None if not found
        """
        db_restaurant = RestaurantCRUD.get_by_id(db, restaurant_id)
        if not db_restaurant:
            return None

        update_data = restaurant_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_restaurant, field, value)

        db.commit()
        db.refresh(db_restaurant)

        return db_restaurant

    @staticmethod
    def delete(db: Session, restaurant_id: int):
        """
        Delete restaurant

        Args:
            db: Database session
            restaurant_id: Restaurant ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_restaurant = RestaurantCRUD.get_by_id(db, restaurant_id)
        if not db_restaurant:
            return False

        db.delete(db_restaurant)
        db.commit()

        return True
