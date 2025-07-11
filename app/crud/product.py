from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.product import Product, Category
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)


class ProductCRUD:

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
        result = await db.execute((select(Product).filter(Product.id == product_id)))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(db: AsyncSession, product_name: str) -> Optional[Product]:
        result = await db.execute(
            (select(Product).filter(Product.name == product_name))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_products(db: AsyncSession) -> List[ProductResponse]:
        result = await db.execute(select(Product))
        products = result.scalars().all()
        return [ProductResponse.from_orm(product) for product in products]

    @staticmethod
    async def get_products_by_category(db: AsyncSession, category_id: int) -> List[ProductResponse]:
        result = await db.execute(
            select(Product).filter(Product.category_id == category_id)
        )
        products = result.scalars().all()
        return [ProductResponse.from_orm(product) for product in products]

    @staticmethod
    async def toggle_availability(
        db: AsyncSession, product_id: int
    ) -> Optional[Product]:
        """Toggle product availability"""
        db_product = await ProductCRUD.get_by_id(db, product_id)
        if not db_product:
            return None

        db_product.is_available = not db_product.is_available
        await db.commit()
        await db.refresh(db_product)

        return db_product

    @staticmethod
    async def create(db: AsyncSession, product_create: ProductCreate) -> Product:
        """
        Create new product

        Args:
            db: Database AsyncSession
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
        await db.commit()
        await db.refresh(db_product)

        return db_product

    @staticmethod
    async def update(
        db: AsyncSession, product_id: int, product_update: ProductUpdate
    ) -> Optional[Product]:
        """
        Update product

        Args:
            db: Database AsyncSession
            product_id: Product ID
            product_update: Data for update

        Returns:
            Product: Updated product or None if not found
        """
        db_product = await ProductCRUD.get_by_id(db, product_id)
        if not db_product:
            return None

        update_data = product_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_product, field, value)

        await db.commit()
        await db.refresh(db_product)

        return db_product

    @staticmethod
    async def delete(db: AsyncSession, product_id: int) -> bool:
        """
        Delete product

        Args:
            db: Database AsyncSession
            product_id: Product ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_product = await ProductCRUD.get_by_id(db, product_id)
        if not db_product:
            return False

        await db.delete(db_product)
        await db.commit()

        return True


class CategoryCRUD:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[CategoryResponse]:
        result = await db.execute(select(Category))
        categories = result.scalars().all()
        return [CategoryResponse.from_orm(category) for category in categories]

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
        result = await db.execute(select(Category).filter(Category.id == category_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(db: AsyncSession, category_name: str) -> Optional[Category]:
        result = await db.execute(
            select(Category).filter(Category.name == category_name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, category_create: CategoryCreate):
        """
        Create new category

        Args:
            db: Database AsyncSession
            category_create: Category creation schema

        Returns:
            Category: Created category
        """
        existing_category = await CategoryCRUD.get_by_name(db, category_create.name)
        if existing_category:
            raise ValueError("Category with this name already exists")

        db_category = Category(name=category_create.name)

        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)

        return db_category

    @staticmethod
    async def update(
        db: AsyncSession, category_id: int, category_update: CategoryUpdate
    ) -> Optional[Category]:
        """
        Update category

        Args:
            db: Database AsyncSession
            category_id: Category ID
            category_update: Data for update

        Returns:
            Category: Updated category or None if not found
        """
        db_category = await CategoryCRUD.get_by_id(db, category_id)
        if not db_category:
            return None

        update_data = category_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_category, field, value)

        await db.commit()
        await db.refresh(db_category)

        return db_category

    @staticmethod
    async def delete(db: AsyncSession, category_id: int) -> bool:
        """
        Delete category

        Args:
            db: Database AsyncSession
            category_id: Category ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_category = await CategoryCRUD.get_by_id(db, category_id)
        if not db_category:
            return False

        result = await db.execute(
            select(func.count())
            .select_from(Product)
            .filter(Product.category_id == category_id)
        )
        products_count = result.scalar_one()
        if products_count > 0:
            raise ValueError("Cannot delete category with existing products")

        await db.delete(db_category)
        await db.commit()

        return True
