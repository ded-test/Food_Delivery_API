from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    products: Mapped["Product"] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    price: Mapped[float] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(default=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    category: Mapped["Category"] = relationship(back_populates="products")
