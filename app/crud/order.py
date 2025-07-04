from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate, OrderItemUpdate


class OrderCRUD:

    def get_by_id(self, db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> List[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()

    def get_open_orders(self, db: Session) -> List[Order]:
        return db.query(Order).filter(Order.status != OrderStatus.COMPLETED).all()

    def get_by_status(self, db: Session, status: OrderStatus) -> List[Order]:
        return db.query(Order).filter(Order.status == status).all()

    def get_all(self, db: Session) -> List[Order]:
        return db.query(Order).order_by(Order.created_at.desc()).all()

    def create(self, db: Session, order_create: OrderCreate) -> Order:
        """
        Create new order

        Args:
            db: Database session
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
            items=[
                OrderItem(
                    product_id=item.product_id, quantity=item.quantity, price=item.price
                )
                for item in order_create.items
            ],
        )

        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        return db_order

    def update(
        self, db: Session, order_id: int, order_update: OrderItemUpdate
    ) -> Optional[Order]:
        """
        Update order

        Args:
            db: Database session
            order_id: Order ID
            order_update: Data for update

        Returns:
            Order: Updated order or None if not found
        """
        db_order = self.get_by_id(db, order_id)
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

        db.commit()
        db.refresh(db_order)

        return db_order

    def delete(self, db: Session, order_id: int) -> bool:
        """
        Delete order

        Args:
            db: Database session
            order_id: Order ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_order = self.get_by_id(db, order_id)
        if not db_order:
            return False

        db.delete(db_order)
        db.commit()

        return True


class OrderItemCRUD:

    def get_by_id(self, db: Session, order_item_id: int) -> Optional[OrderItem]:
        return db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    def get_by_order_id(self, db: Session, order_id: int) -> Optional[OrderItem]:
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).first()

    def create(self, db: Session, order_item_create: OrderItemCreate) -> OrderItem:
        """
        Create new OrderItem

        Args:
            db: Database session
            order_item_create: OrderItem creation schema

        Returns:
            OrderItem: Created order_item
        """

        db_order_item = OrderItem(
            product_id=order_item_create.product_id,
            quantity=order_item_create.quantity,
            price_per_item=order_item_create.price_per_item,
        )

        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)

        return db_order_item

    def update(
        self, db: Session, order_id: int, order_update: OrderUpdate
    ) -> Optional[Order]:
        db_order = self.get_by_id(db, order_id)
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
                        price_per_item=item.price_per_item,
                    )
                )
            db_order.total_amount = sum(
                i.price_per_item * i.quantity for i in update_data["items"]
            )
            update_data.pop("items")

        for field, value in update_data.items():
            setattr(db_order, field, value)

        db.commit()
        db.refresh(db_order)
        return db_order

    def delete(self, db: Session, order_item_id: int) -> bool:
        """
        Delete an OrderItem by its ID.
        Args:
            db: Database session
            order_item_id: ID of the OrderItem
         Returns:
            bool: True if deleted, False if not found
        """
        db_item = self.get_by_id(db, order_item_id)
        if not db_item:
            return False

        db.delete(db_item)
        db.commit()
        return True
