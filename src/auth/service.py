from .models import User
from .schemas import UserCreateModel
from .utils import generate_passwd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.execute(statement)

        user = result.scalar()

        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel,session: AsyncSession ):
        user_data_dict = user_data.model_dump()

        new_user = User(
            first_name=user_data_dict['first_name'],
            last_name=user_data_dict['last_name'],
            email=user_data_dict["email"],
            username=user_data_dict["username"]
        )

        new_user.hashed_password = generate_passwd_hash(user_data_dict['password'])

        session.add(new_user)

        await session.commit()
        return new_user



