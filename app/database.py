from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings
from models.base import Base

DATABASE_URL = settings.DATABASE_URL


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _initialized: bool = False

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

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
        print("✅ Database tables created successfully")

    async def drop_tables(self):
        """Drop all database tables (useful for testing)"""
        if not self.engine:
            raise RuntimeError("Database not initialized! Call init_db() first")

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("✅ Database tables dropped successfully")

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


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.get_session() as session:
        yield session
