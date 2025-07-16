from typing import Optional, List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
import hashlib

from app.core.security import verify_password
from app.models.user import User, UserAddress
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserChangePassword,
    UserAddressCreate,
    UserAddressUpdate,
    UserAddressResponse,
    UserLogin,
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
    async def get_by_name(db: AsyncSession, name: str) -> Optional[User]:
        result = await db.execute(select(User).filter(User.first_name == name))
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
    async def login(db: AsyncSession, user_login: UserLogin) -> Optional[User]:
        """
        Authenticate user login

        Args:
            db: Database AsyncSession
            user_login: User login schema

        Returns:
            User: Authenticated user if credentials are valid, None otherwise
        """
        db_user = await UserCRUD.get_by_number(db, user_login.number)
        if not db_user:
            return None

        if not verify_password(user_login.password, db_user.password_hash):
            return None

        return db_user

    @staticmethod
    async def authenticate_user_login(
        db: AsyncSession, number: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user by number and password

        Args:
            db: Database AsyncSession
            number: Phone number
            password: Plain password

        Returns:
            User: Authenticated user if credentials are valid, None otherwise
        """
        user_login = UserLogin(number=number, password=password)
        return await UserCRUD.login(db, user_login)

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

        if not await UserCRUD._verify_password(
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
    async def authenticate(
        db: AsyncSession, number: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user

        Args:
            db: Database AsyncSession
            number: Phone number
            password: Password

        Returns:
            User: User if authentication successful, otherwise None
        """
        db_user = await UserCRUD.get_by_number(db, number)
        if not db_user:
            return None

        if not await UserCRUD._verify_password(
            password, db_user.password_salt, db_user.password_hash
        ):
            return None

        return db_user


class UserAddressCRUD:

    @staticmethod
    async def get_by_id(
        db: AsyncSession, user_address_id: int
    ) -> Optional[UserAddress]:
        result = await db.execute(
            select(UserAddress).filter(UserAddress.id == user_address_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> List[UserAddress]:
        result = await db.execute(
            select(UserAddress).filter(UserAddress.user_id == user_id)
        )
        addresses = result.scalars().all()
        return [UserAddressResponse.from_orm(address) for address in addresses]

    @staticmethod
    async def create(
        db: AsyncSession, user_id: int, user_address_create: UserAddressCreate
    ) -> UserAddress:
        """
        Create new address for user

        Args:
            db: Database AsyncSession
            user_id: User ID
            user_address_id: Address creation data

        Returns:
            UserAddress: Created address
        """
        db_address = UserAddress(user_id=user_id, **user_address_create.model_dump())

        db.add(db_address)
        await db.commit()
        await db.refresh(db_address)

        return db_address

    @staticmethod
    async def update(
        db: AsyncSession, user_address_id: int, user_address_update: UserAddressUpdate
    ) -> Optional[UserAddress]:
        """
        Create new address for user

        Args:
            db: Database AsyncSession
            user_address_id: user address ID
            user_address_update: Address updating data
        Returns:
            UserAddress: updating address
        """
        db_address = await UserAddressCRUD.get_by_id(db, user_address_id)
        if not db_address:
            return None

        update_data = user_address_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_address, field, value)

        await db.commit()
        await db.refresh(db_address)

        return db_address

    @staticmethod
    async def delete(db: AsyncSession, user_address_id: int) -> bool:
        db_address = await UserAddressCRUD.get_by_id(db, user_address_id)
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
