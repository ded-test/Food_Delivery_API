from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantCRUD:

    def get_by_id(self, db: Session, restaurant_id: int) -> Optional[Restaurant]:
        return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def get_by_name(self, db: Session, restaurant_name: str) -> List[Restaurant]:
        return db.query(Restaurant).filter(Restaurant.name == restaurant_name).all()

    def create(self, db: Session, restaurant_create: RestaurantCreate) -> Restaurant:
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

    def update(
        self, db: Session, restaurant_id: int, restaurant_update: RestaurantUpdate
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
        db_restaurant = self.get_by_id(db, restaurant_id)
        if not db_restaurant:
            return None

        update_data = restaurant_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_restaurant, field, value)

        db.commit()
        db.refresh(db_restaurant)

        return db_restaurant

    def delete(self, db: Session, restaurant_id: int):
        """
        Delete restaurant

        Args:
            db: Database session
            restaurant_id: Restaurant ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_restaurant = self.get_by_id(db, restaurant_id)
        if not db_restaurant:
            return False

        db.delete(db_restaurant)
        db.commit()

        return True
