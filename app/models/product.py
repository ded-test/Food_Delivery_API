from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")
