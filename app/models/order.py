from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum


class OrderStatus(enum.Enum):
    NEW = "new"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.NEW, nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)

    delivery_address = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_per_item = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

