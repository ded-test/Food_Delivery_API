from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    number = Column(String, unique=True)
    password_salt = Column(String(64), nullable=False)
    password_hash = Column(String(128), nullable=False)


    addresses = relationship("UserAddress", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, number='{self.number}', name='{self.first_name} {self.last_name}')>"


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    street = Column(String(100), nullable=False)
    house_number = Column(String(20), nullable=False)
    apartment = Column(String(20), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<UserAddress(id={self.id}, user_id={self.user_id}, city='{self.city}')>"
