from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from src.books.routes import books_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.db.database import init_db
from .errors import (
    create_exception_handler,
    InvalidCredentials,
    TagNotFound,
    BookNotFound,
    UserAlreadyExists,
    UserNotFound,
    InsufficientPermission,
    AccessTokenRequired,
    InvalidToken,
    RefreshTokenRequired,
    RevokedToken
)

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

# --- Register Exception Handlers ---

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User with that email already exists.",
            "error_code": "USER_ALREADY_EXISTS",
        }
    )
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Bhai, ye book database mein nahi mili.",
            "error_code": "BOOK_NOT_FOUND",
        }
    )
)

app.add_exception_handler(
    TagNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Tag not found.",
            "error_code": "TAG_NOT_FOUND",
        }
    )
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "User with that email doesn't exist.",
            "error_code": "USER_NOT_FOUND",
        }
    )
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "message": "Email ya password galat hai bhai.",
            "error_code": "INVALID_CREDENTIALS",
        }
    )
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token is invalid or expired.",
            "resolution": "Please get a new token",
            "error_code": "INVALID_TOKEN",
        }
    )
)

app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token is invalid or has been revoked (Logged out).",
            "error_code": "TOKEN_REVOKED",
        }
    )
)

app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Please provide an access token.",
            "resolution": "Login to get an access token",
            "error_code": "ACCESS_TOKEN_REQUIRED",
        }
    )
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Please provide a valid refresh token.",
            "resolution": "Use your refresh token to get a new access token",
            "error_code": "REFRESH_TOKEN_REQUIRED",
        }
    )
)

app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Bhai, tere paas ye action karne ki permission nahi hai.",
            "error_code": "INSUFFICIENT_PERMISSION",
        }
    )
)

@app.exception_handlers(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        content={"message": "Oops! Something went wrong", "error_code": "INTERNAL_SERVER_ERROR"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

app.include_router(books_router, prefix="/api/v1/books", tags=["Books"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(review_router, prefix="/api/v1/reviews", tags=["Reviews"])