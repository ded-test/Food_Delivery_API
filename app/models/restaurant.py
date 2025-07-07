from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    street: Mapped[str] = mapped_column(nullable=False)
    house_number: Mapped[str] = mapped_column(nullable=False)
    apartment: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
