from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from app.core.config import settings
from app.core.database import db_manager, redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    try:
        print("Initializing database...")
        db_manager.init_db(settings.DATABASE_URL)

        print("Creating database tables...")
        await db_manager.create_tables()

        print("Initializing Redis...")
        await redis_manager.init_redis(settings.REDIS_URL)

        print("Testing connections...")
        await _test_connections()

        print("All services initialized successfully!")

    except Exception as e:
        print(f"Startup failed: {e}")
        await _cleanup()
        raise

    yield

    print("Application shutdown...")
    await _cleanup()
    print("Application stopped successfully")


async def _test_connections():
    """Connection testing"""

    # test PostgreSQL
    try:
        async with db_manager.get_session() as session:
            await session.execute(select(1))
        print("PostgreSQL connection OK")
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        raise

    # test Redis
    try:
        async with redis_manager.get_client() as redis:
            redis.ping()
        print("Redis connection OK")
    except Exception as e:
        print(f"Redis connection failed: {e}")
        raise


async def _cleanup():
    """Cleaning up resources"""
    try:
        # Closing Redis
        await redis_manager.close()
        print("Redis connections closed")

        # Closing PostgreSQL
        await db_manager.close()
        print("Database connections closed")

    except Exception as e:
        print(f"Cleanup warning: {e}")


main_app = FastAPI(lifespan=lifespan)


@main_app.post("/")
async def hello():
    return {"message": "Hello!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:main_app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
