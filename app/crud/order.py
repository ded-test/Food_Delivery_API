from typing import Optional, List, Any, Coroutine, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Order
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderItemUpdate,
    OrderResponse, OrderItemResponse,
)


class OrderCRUD:

    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
        result = await db.execute(select(Order).filter(Order.id == order_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_last_order_by_user_id(
        db: AsyncSession, user_id: int
    ) -> Optional[Order]:
        result = await db.execute(
            select(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_open_orders(db: AsyncSession, user_id: int) -> List[OrderResponse]:
        result = await db.execute(
            select(Order)
            .filter(Order.status != OrderStatus.COMPLETED)
            .filter(Order.status != OrderStatus.CANCELED)
            .filter(Order.user_id == user_id)
        )
        orders = result.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]

    @staticmethod
    async def _get_open_orders(db: AsyncSession) -> List[OrderResponse]:
        """
        Returns all open orders, without user_id
        """
        result = await db.execute(
            select(Order)
            .filter(Order.status != OrderStatus.COMPLETED)
            .filter(Order.status != OrderStatus.CANCELED)
        )
        orders = result.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]

    @staticmethod
    async def get_by_status(db: AsyncSession, status: OrderStatus, user_id: int) -> List[OrderResponse]:
        result = await db.execute(select(Order).filter(Order.status == status))
        orders = result.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]

    @staticmethod
    async def _get_by_status(db: AsyncSession, status: OrderStatus) -> List[OrderResponse]:
        """
        Returns all {status} orders, without user_id
        """
        result = await db.execute(select(Order).filter(Order.status == status))
        orders = result.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]

    @staticmethod
    async def get_all(db: AsyncSession, user_id: int) -> List[OrderResponse]:
        result = await db.execute(
            select(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        orders = result.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]

    @staticmethod
    async def _get_all(db: AsyncSession) -> List[OrderResponse]:
        """
        Returns all orders, without user_id
        """
        result = await db.execute(select(Order).order_by(Order.created_at.desc()))
        orders = result.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]

    @staticmethod
    async def create(db: AsyncSession, order_create: OrderCreate) -> Order:
        """
        Create new order

        Args:
            db: Database AsyncSession
            order_create: Order creation schema

        Returns:
            Order: Created order
        """
        total_amount = sum(item.price * item.quantity for item in order_create.items)

        db_order = Order(
            user_id=order_create.user_id,
            status=OrderStatus.NEW,
            total_amount=total_amount,
            delivery_address=order_create.delivery_address,
        )

        for item in order_create.items:
            order_item = OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            db_order.items.append(order_item)

        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)

        return db_order

    @staticmethod
    async def update(
        db: AsyncSession, order_id: int, order_update: OrderUpdate
    ) -> Optional[Order]:
        """
        Update order

        Args:
            db: Database AsyncSession
            order_id: Order ID
            order_update: Data for update

        Returns:
            Order: Updated order or None if not found
        """
        db_order = await OrderCRUD.get_by_id(db, order_id)
        if not db_order:
            return None

        update_data = order_update.model_dump(exclude_unset=True)

        if "items" in update_data:
            db_order.items.clear()
            for item in update_data["items"]:
                db_order.items.append(
                    OrderItem(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                    )
                )

            db_order.total_amount = sum(
                i.price * i.quantity for i in update_data["items"]
            )
            update_data.pop("items")

        await db.commit()
        await db.refresh(db_order)

        return db_order

    @staticmethod
    async def delete(db: AsyncSession, order_id: int) -> bool:
        """
        Delete order

        Args:
            db: Database AsyncSession
            order_id: Order ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_order = await OrderCRUD.get_by_id(db, order_id)
        if not db_order:
            return False

        await db.delete(db_order)
        await db.commit()

        return True


class OrderItemCRUD:

    @staticmethod
    async def get_by_id(db: AsyncSession, order_item_id: int) -> Optional[OrderItem]:
        result = await db.execute(
            select(OrderItem).filter(OrderItem.id == order_item_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_order_id(db: AsyncSession, order_id: int) -> List[OrderItemResponse]:
        result = await db.execute(
            select(OrderItem).filter(OrderItem.order_id == order_id)
        )
        orders = result.scalars().all()
        return [OrderItemResponse.from_orm(order) for order in orders]

    @staticmethod
    async def create(db: AsyncSession, order_item_create: OrderItemCreate) -> OrderItem:
        """
        Create new OrderItem

        Args:
            db: Database AsyncSession
            order_item_create: OrderItem creation schema

        Returns:
            OrderItem: Created order_item
        """

        db_order_item = OrderItem(
            product_id=order_item_create.product_id,
            quantity=order_item_create.quantity,
            price=order_item_create.price,
        )

        db.add(db_order_item)
        await db.commit()
        await db.refresh(db_order_item)

        return db_order_item

    @staticmethod
    async def update(
        db: AsyncSession, order_item_id: int, item_update: OrderItemUpdate
    ) -> Optional[OrderItem]:
        db_item = await OrderItemCRUD.get_by_id(db, order_item_id)
        if not db_item:
            return None

        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def delete(db: AsyncSession, order_item_id: int) -> bool:
        """
        Delete an OrderItem by its ID.
        Args:
            db: Database AsyncSession
            order_item_id: ID of the OrderItem
         Returns:
            bool: True if deleted, False if not found
        """
        db_item = await OrderItemCRUD.get_by_id(db, order_item_id)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True
