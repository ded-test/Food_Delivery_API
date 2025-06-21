from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    street = Column(String(100), nullable=False)
    house_number = Column(String(20), nullable=False)
    apartment = Column(String(20), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
