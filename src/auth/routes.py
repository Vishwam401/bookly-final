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
from .schemas import UserBooksModel, UserCreateModel, UserLoginModel, UserModel, EmailModel
from .service import UserService
from .utils import create_access_token, verify_password, create_url_safe_token, decode_url_safe_token
from src.db.database import get_session
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from src.mail import mail, create_message
from src.config import Config
from src.db.database import get_session


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

REFRESH_TOKEN_EXPIRY_DAYS = 2  # how long refresh token lasts

@auth_router.post('/send_mail')
async def sending_mail(emails:EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"

    message = create_message(
        recipient=emails,
        subject="Welcome",
        body=html,
    )

    await mail.send_message(message)

    return {"message": "Email sent successfully"}


@auth_router.post("/signup",  status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email
    user_exists = await user_service.user_exists(user_data.email, session)

    if user_exists:
        raise UserAlreadyExists

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email":email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>verify your Email<h2>
    <p>Please click this <a href="{link}">link</a> to verify your email:</p>
    """

    message = create_message(
        recipient=[email],
        subject="Verify your Email",
        body=html_message,
    )

    await mail.send_message(message)

    return {
        "message":"Account Created! Check email to verify your account",
        "user":new_user
    }


@auth_router.get('/verify/{token}')
async def verify_user_account(token:str, session:AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {'is_verified': True}, session)

        return JSONResponse(content = {
            "message": "Account verified successfully"},
            status_code = status.HTTP_200_OK,
        )

    return JSONResponse(content = {
        "message": "Account not verified successfully"},
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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