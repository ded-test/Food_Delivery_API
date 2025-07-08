from typing import Optional, List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
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

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_number(db: AsyncSession, number: str) -> Optional[User]:
        result = await db.execute(select(User).filter(User.number == number))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_create: UserCreate) -> User:
        """
        Create new user

        Args:
            db: Database AsyncSession
            user_create: User creation schema

        Returns:
            User: Created user
        """
        salt, password_hash = user_create.create_password_hash()

        existing_user = await UserCRUD.get_by_number(db, user_create.number)
        if existing_user:
            raise ValueError("User with this number already exists.")

        db_user = User(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            number=user_create.number,
            password_salt=salt,
            password_hash=password_hash,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def update(
        db: AsyncSession, user_id: int, user_update: UserUpdate
    ) -> Optional[User]:
        """
        Update user

        Args:
            db: Database AsyncSession
            user_id: User ID
            user_update: Data for update

        Returns:
            User: Updated user or None if not found
        """
        db_user = await UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def change_password(
        db: AsyncSession, user_id: int, password_change: UserChangePassword
    ) -> Optional[User]:
        """
        Change user password

        Args:
            db: Database AsyncSession
            user_id: User ID
            password_change: Password change data

        Returns:
            User: User with updated password or None
        """
        db_user = await UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return None

        if not UserCRUD._verify_password(
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

        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """
        Delete user

        Args:
            db: Database AsyncSession
            user_id: User ID

        Returns:
            bool: True if deleted, False if not found
        """
        db_user = await UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()

        return True

    @staticmethod
    async def _verify_password(
        plain_password: str, salt: str, hashed_password: str
    ) -> bool:
        """Verify password"""
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()

        return password_hash == hashed_password

    @staticmethod
    async def authenticate(db: AsyncSession, number: str, password: str) -> Optional[User]:
        """
        Authenticate user

        Args:
            db: Database AsyncSession
            number: Phone number
            password: Password

        Returns:
            User: User if authentication successful, otherwise None
        """
        user = await UserCRUD.get_by_number(db, number)
        if not user:
            return None

        if not UserCRUD._verify_password(password, user.password_salt, user.password_hash):
            return None

        return user


class UserAddressCRUD:

    @staticmethod
    async def get_by_id(db: AsyncSession, address_id: int) -> Optional[UserAddress]:
        result = await db.execute(select(UserAddress).filter(UserAddress.id == address_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> Sequence[UserAddress]:
        result = await db.execute(select(UserAddress).filter(UserAddress.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession, user_id: int, address_create: UserAddressCreate
    ) -> UserAddress:
        """
        Create new address for user

        Args:
            db: Database AsyncSession
            user_id: User ID
            address_create: Address creation data

        Returns:
            UserAddress: Created address
        """
        db_address = UserAddress(user_id=user_id, **address_create.model_dump())

        db.add(db_address)
        await db.commit()
        await db.refresh(db_address)

        return db_address

    @staticmethod
    async def update(
        db: AsyncSession, address_id: int, address_update: UserAddressUpdate
    ) -> Optional[UserAddress]:
        db_address = await UserAddressCRUD.get_by_id(db, address_id)
        if not db_address:
            return None

        update_data = address_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_address, field, value)

        await db.commit()
        await db.refresh(db_address)

        return db_address

    @staticmethod
    async def delete(db: AsyncSession, address_id: int) -> bool:
        db_address = await UserAddressCRUD.get_by_id(db, address_id)
        if not db_address:
            return False

        await db.delete(db_address)
        await db.commit()

        return True

    @staticmethod
    async def delete_by_user_id(db: AsyncSession, user_id: int) -> int:
        result = await db.execute(
            delete(UserAddress)
            .where(UserAddress.user_id == user_id)
            .returning(UserAddress.id)
        )
        await db.commit()
        return len(result.fetchall())