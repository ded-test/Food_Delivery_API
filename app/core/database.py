from contextlib import asynccontextmanager
from typing import AsyncGenerator
import redis
from typing import Optional, TypeVar, Type
import threading

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.base import Base

DATABASE_URL = settings.DATABASE_URL
REDIS_URL = settings.REDIS_URL

# typing for correct handling of inheritance
S = TypeVar("S", bound="SingletonMeta")

"""
TypeVar is a special mechanism that allows you to 
create generalized (generic) types.

bound='SingletonMeta' means that T can only be 
a type that inherits from SingletonMeta

The problem without typing:
Without typing, the __new__ method will simply return 
object, which loses information about the specific class.
"""


class SingletonMeta:
    _instances = {}
    _lock = threading.Lock()

    # Double-Checked Locking
    def __new__(cls: Type[S]) -> S:
        if cls not in cls._instances:  # first check (without blocking)
            with cls._lock:  # lock capture
                if cls not in cls._instances:  # second check (under lockdown)
                    cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class DatabaseManager(SingletonMeta):
    _initialized = False

    def __init__(self):
        # Initialize only once
        if not DatabaseManager._initialized:
            self.engine = None
            self.session_factory = None
            self._database_url = None
            DatabaseManager._initialized = True

    def init_db(self, database_url: str):
        """Initialize the database engine and session factory"""
        if self.engine is not None:
            print(f"Database already initialized with URL: {self._database_url}")
            return

        self.engine = create_async_engine(
            database_url,
            echo=True,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )
        self._database_url = database_url
        print(f"Database initialized: {database_url}")

    async def create_tables(self):
        """Create all database tables"""
        if not self.engine:
            raise RuntimeError("Database not initialized! Call init_db() first")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully")

    async def drop_tables(self):
        """Drop all database tables (useful for testing)"""
        if not self.engine:
            raise RuntimeError("Database not initialized! Call init_db() first")

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("Database tables dropped successfully")

    async def recreate_tables(self):
        """Drop and recreate all tables"""
        await self.drop_tables()
        await self.create_tables()

    async def close(self):
        """Close database connections"""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None
            self._database_url = None
            print("DatabaseManager closed")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager for database session"""
        if not self.session_factory:
            raise RuntimeError("Database not initialized! Call init_db() first")

        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db_manager = DatabaseManager()


class RedisManager(SingletonMeta):
    _initialized = False

    def __init__(self):
        if not RedisManager._initialized:
            self.redis = None
            self._database_url = None
            RedisManager._initialized = True

    async def init_redis(self, database_url: str):
        if self.redis is not None:
            print(f"Redis already initialized with URL: {self._database_url}")
            return

        try:
            self.redis = redis.from_url(
                database_url, decode_responses=True, encoding="utf-8"
            )
            self.redis.ping()
            self._database_url = database_url
            print(f"Redis initialized: {database_url}")
        except Exception as e:
            self.redis = None
            raise RuntimeError(f"Redis initialization failed: {e}")

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        if not self.redis:
            raise RuntimeError("Redis not initialized! Call init_redis() first")
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[str]:
        if not self.redis:
            raise RuntimeError("Redis not initialized! Call init_redis() first")
        return await self.redis.get(key)

    async def delete(self, key: str):
        if not self.redis:
            raise RuntimeError("Redis not initialized! Call init_redis() first")
        await self.redis.delete(key)

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.aclose()  # Изменено для redis-py
            self.redis = None
            self._database_url = None
            print("RedisManager closed")

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[redis.Redis, None]:
        """Context manager for Redis client"""
        if not self.redis:
            raise RuntimeError("Redis not initialized! Call init_redis() first")

        try:
            yield self.redis
        finally:
            pass


redis_manager = RedisManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.get_session() as session:
        yield session


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    async with redis_manager.get_client() as redis_client:
        yield redis_client
