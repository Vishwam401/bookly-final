from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class BooklyException(Exception):
    """This is the base class for all bookly errors"""
    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a token that was revoked from the system"""
    pass

class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when access is required"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has provided a access token when refresh is required"""
    pass

class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who already exists."""
    pass

class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during login."""
    pass

class InsufficientPermission(BooklyException):
    """User does not have the required permissions to perform an action."""
    pass

class BookNotFound(BooklyException):
    """Book not found."""
    pass

class TagNotFound(BooklyException):
    """Tag not found."""
    pass

class UserNotFound(BooklyException):
    """User not found."""
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: BooklyException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
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

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )