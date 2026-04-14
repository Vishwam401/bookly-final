from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_passwd_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        user_dict = user_data.model_dump()

        new_user = User(
            first_name=user_dict["first_name"],
            last_name=user_dict["last_name"],
            email=user_dict["email"],
            username=user_dict["username"],
            hashed_password=generate_passwd_hash(user_dict["password"]),
            role="user",
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user


    async def update_user(self, user:User, user_data: dict, session: AsyncSession):

        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user