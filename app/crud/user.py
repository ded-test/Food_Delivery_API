from typing import Optional, List
from sqlalchemy.orm import Session
import hashlib

from app.models.user import User, UserAddress
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserChangePassword,
    UserAddressCreate,
    UserAddressUpdate,
)


class UserCRUD:

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_number(self, db: Session, number: str) -> Optional[User]:
        return db.query(User).filter(User.number == number).first()

    def create(self, db: Session, user_create: UserCreate) -> User:
        """
        Create new user

        Args:
            db: Database session
            user_create: User creation schema

        Returns:
            User: Created user
        """
        salt, password_hash = user_create.create_password_hash()

        db_user = User(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            number=user_create.number,
            password_salt=salt,
            password_hash=password_hash,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def update(
        self, db: Session, user_id: int, user_update: UserUpdate
    ) -> Optional[User]:
        """
        Update user

        Args:
            db: Database session
            user_id: User ID
            user_update: Data for update

        Returns:
            User: Updated user or None if not found
        """
        db_user = self.get_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)

        return db_user

    def change_password(
        self, db: Session, user_id: int, password_change: UserChangePassword
    ) -> Optional[User]:
        """
        Change user password

        Args:
            db: Database session
            user_id: User ID
            password_change: Password change data

        Returns:
            User: User with updated password or None
        """
        db_user = self.get_by_id(db, user_id)
        if not db_user:
            return None

        if not self.verify_password(
            password_change.current_password,
            db_user.password_salt,
            db_user.password_hash,
        ):
            raise ValueError("Invalid current password")

        salt, password_hash = password_change.create_password_hash(
            password_change.new_password
        )

        db_user.password_salt = salt
        db_user.password_hash = password_hash

        db.commit()
        db.refresh(db_user)

        return db_user

    def delete(self, db: Session, user_id: int) -> bool:
        """
        Delete user

        Args:
            db: Database session
            user_id: User ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_user = self.get_by_id(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()

        return True

    def verify_password(
        self, plain_password: str, salt: str, hashed_password: str
    ) -> bool:
        """Verify password"""
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()

        return password_hash == hashed_password

    def authenticate(self, db: Session, number: str, password: str) -> Optional[User]:
        """
        Authenticate user

        Args:
            db: Database session
            number: Phone number
            password: Password

        Returns:
            User: User if authentication successful, otherwise None
        """
        user = self.get_by_number(db, number)
        if not user:
            return None

        if not self.verify_password(password, user.password_salt, user.password_hash):
            return None

        return user


class UserAddressCRUD:

    def get_by_id(self, db: Session, address_id: int) -> Optional[UserAddress]:
        return db.query(UserAddress).filter(UserAddress.id == address_id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> List[UserAddress]:
        return db.query(UserAddress).filter(UserAddress.user_id == user_id).all()

    def create(
        self, db: Session, user_id: int, address_create: UserAddressCreate
    ) -> UserAddress:
        """
        Create new address for user

        Args:
            db: Database session
            user_id: User ID
            address_create: Address creation data

        Returns:
            UserAddress: Created address
        """
        db_address = UserAddress(user_id=user_id, **address_create.model_dump())

        db.add(db_address)
        db.commit()
        db.refresh(db_address)

        return db_address

    def update(
        self, db: Session, address_id: int, address_update: UserAddressUpdate
    ) -> Optional[UserAddress]:
        db_address = self.get_by_id(db, address_id)
        if not db_address:
            return None

        update_data = address_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_address, field, value)

        db.commit()
        db.refresh(db_address)

        return db_address

    def delete(self, db: Session, address_id: int) -> bool:
        db_address = self.get_by_id(db, address_id)
        if not db_address:
            return False

        db.delete(db_address)
        db.commit()

        return True

    def delete_by_user_id(self, db: Session, user_id: int) -> int:
        count = db.query(UserAddress).filter(UserAddress.user_id == user_id).count()
        db.query(UserAddress).filter(UserAddress.user_id == user_id).delete()
        db.commit()

        return count
