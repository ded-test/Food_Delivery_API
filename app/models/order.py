import enum
from datetime import datetime
from typing import List

from sqlalchemy import Float, ForeignKey, String, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base


class OrderStatus(enum.Enum):
    NEW = "new"
    PROCESSING = "processing"
    DELIVERY = "delivery"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.NEW
    )
    total_amount: Mapped[float] = mapped_column(default=0.0)

    delivery_address: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Many-to-One
    user: Mapped["User"] = relationship(back_populates="orders")
    # One-to-Many
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    price: Mapped[float] = mapped_column(nullable=False)

    # Many-to-One
    order: Mapped["Order"] = relationship(back_populates="items")
    # Many-to-One
    product: Mapped["Product"] = relationship()
