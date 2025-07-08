import enum
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import Base


class GenderEnum(str, enum.Enum):
    MALE = "man"
    FEMALE = "woman"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[GenderEnum]
    years: Mapped[int] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_salt: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    # One-to-Many
    addresses: Mapped[List["UserAddress"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    # One-to-Many
    orders: Mapped[List["Order"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, number='{self.number}', name='{self.first_name} {self.last_name}')>"


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    street: Mapped[str] = mapped_column(nullable=False)
    house_number: Mapped[str] = mapped_column(nullable=False)
    apartment: Mapped[str | None]
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

    # Many-to-One
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self):
        return (
            f"<UserAddress(id={self.id}, user_id={self.user_id}, city='{self.city}')>"
        )
