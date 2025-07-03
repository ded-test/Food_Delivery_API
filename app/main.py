from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import DATABASE_URL, db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    db_manager.init_db(DATABASE_URL)

    await db_manager.create_tables()
    print("Database initialized")

    yield

    print("Application shutdown...")
    await db_manager.close()
    print("Database connections are closed")


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
