from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from src.books.routes import books_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.db.database import init_db
from .errors import register_all_errors
from .middleware import register_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("Server has been stopped")


app = FastAPI(
    title="Bookly API",
    description="A REST API for managing books, reviews, and tags",
    version="v1",
    lifespan=lifespan,
)


register_all_errors(app)

register_middleware(app)

app.include_router(books_router, prefix="/api/v1/books", tags=["Books"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(review_router, prefix="/api/v1/reviews", tags=["Reviews"])

