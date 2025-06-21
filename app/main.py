from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import db_manager, DATABASE_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application startup...")
    db_manager.init_db(DATABASE_URL)

    await db_manager.create_tables()
    print("Database initialized")

    yield

    print("Application shutdown...")
    await db_manager.close()
    print("Database connections are closed")

app = FastAPI(lifespan=lifespan)

@app.post("/")
async def hello():
    return {"message":"Hello!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )