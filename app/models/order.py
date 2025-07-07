import enum
from datetime import datetime
from typing import List

from sqlalchemy import Float, ForeignKey, String, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models import Product, User
from app.models.base import Base


class OrderStatus(enum.Enum):
    NEW = "new"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.NEW
    )
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)

    delivery_address: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    price_per_item: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
