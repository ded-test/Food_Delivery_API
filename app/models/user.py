from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    number = Column(String, unique=True)

    addresses = relationship("UserAddress", back_populates="user")


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    street = Column(String(100), nullable=False)
    house_number = Column(String(20), nullable=False)
    apartment = Column(String(20), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)

    user = relationship("User", back_populates="addresses")
