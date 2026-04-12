from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from .schemas import UserBooksModel, UserCreateModel, UserLoginModel, UserModel
from .service import UserService
from .utils import create_access_token, verify_password
from src.db.database import get_session
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

REFRESH_TOKEN_EXPIRY_DAYS = 2  # how long refresh token lasts


@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    user_exists = await user_service.user_exists(user_data.email, session)

    if user_exists:
        raise UserAlreadyExists

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.get_user_by_email(login_data.email, session)

    if user and verify_password(login_data.password, user.hashed_password):
        access_token = create_access_token(
            user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role}
        )
        refresh_token = create_access_token(
            user_data={"email": user.email, "user_uid": str(user.uid)},
            refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
        )
        return JSONResponse(
            content={
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"email": user.email, "uid": str(user.uid)},
            }
        )

    raise InvalidCredentials


@auth_router.get("/refresh-token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken


@auth_router.get("/me", response_model=UserBooksModel)
async def get_me(
    user: UserBooksModel = Depends(get_current_user),
    _: bool = Depends(role_checker),
):
    return user


@auth_router.post("/logout")
async def revoke_token(token_details: dict = Depends(RefreshTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "Logged out successfully"},
        status_code=status.HTTP_200_OK,
    )