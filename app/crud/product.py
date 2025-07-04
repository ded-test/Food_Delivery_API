from typing import Optional
from sqlalchemy.orm import Session

from app.models.product import Product, Category
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    CategoryCreate,
    CategoryUpdate,
)


class ProductCRUD:

    def get_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    def get_by_name(self, db: Session, product_name: str) -> Optional[Product]:
        return db.query(Product).filter(Product.name == product_name).first()

    def toggle_availability(self, db: Session, product_id: int) -> Optional[Product]:
        """Toggle product availability"""
        db_product = self.get_by_id(db, product_id)
        if not db_product:
            return None

        db_product.is_available = not db_product.is_available
        db.commit()
        db.refresh(db_product)

        return db_product

    def create(self, db: Session, product_create: ProductCreate) -> Product:
        """
        Create new product

        Args:
            db: Database session
            product_create: Product creation schema

        Returns:
            Product: Created product
        """
        db_product = Product(
            name=product_create.name,
            description=product_create.description,
            price=product_create.price,
            is_available=product_create.is_available,
            category_id=product_create.category_id,
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    def update(
        self, db: Session, product_id: int, product_update: ProductUpdate
    ) -> Optional[Product]:
        """
        Update product

        Args:
            db: Database session
            product_id: Product ID
            product_update: Data for update

        Returns:
            Product: Updated product or None if not found
        """
        db_product = self.get_by_id(db, product_id)
        if not db_product:
            return None

        update_data = product_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_product, field, value)

        db.commit()
        db.refresh(db_product)

        return db_product

    def delete(self, db: Session, product_id: int) -> bool:
        """
        Delete product

        Args:
            db: Database session
            product_id: Product ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_product = self.get_by_id(db, product_id)
        if not db_product:
            return False

        db.delete(db_product)
        db.commit()

        return True


class CategoryCRUD:

    def get_by_id(self, db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, db: Session, category_name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == category_name).first()

    def create(self, db: Session, category_create: CategoryCreate):
        """
        Create new category

        Args:
            db: Database session
            category_create: Category creation schema

        Returns:
            Category: Created category
        """
        existing_category = self.get_by_name(db, category_create.name)
        if existing_category:
            raise ValueError("Category with this name already exists")

        db_category = Category(name=category_create.name)

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category

    def update(
        self, db: Session, category_id: int, category_update: CategoryUpdate
    ) -> Optional[Category]:
        """
        Update category

        Args:
            db: Database session
            category_id: Category ID
            category_update: Data for update

        Returns:
            Category: Updated category or None if not found
        """
        db_category = self.get_by_id(db, category_id)
        if not db_category:
            return None

        update_data = category_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_category, field, value)

        db.commit()
        db.refresh(db_category)

        return db_category

    def delete(self, db: Session, category_id: int) -> bool:
        """
        Delete category

        Args:
            db: Database session
            category_id: Category ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_category = self.get_by_id(db, category_id)
        if not db_category:
            return False

        products_count = (
            db.query(Product).filter(Product.category_id == category_id).count()
        )
        if products_count > 0:
            raise ValueError("Cannot delete category with existing products")

        db.delete(db_category)
        db.commit()

        return True
