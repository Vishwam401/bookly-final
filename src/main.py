
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import init_db
from src.books.routes import books_router
from src.auth.routes import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server is starting...")

    await init_db()

    yield

    print("🛑 Server has been stopped")

# ✅ App metadata
app = FastAPI(
    title="Bookly API",
    description="A REST API for managing books",
    version="v1",
)

# ✅ Router include (prefix + tags)
app.include_router(
    books_router,
    prefix="/api/v1/books",
    tags=["Books"]
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["auth"]
)