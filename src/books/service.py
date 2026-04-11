from sqlmodel import select
from ..db.models import Book
from datetime import datetime
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession


class BookService:

    # 1. Saari books laane ke liye (Pagination ke sath)
    async def get_all_books(self, limit: int, offset: int, session: AsyncSession):
        # Query mein limit aur offset apply karo
        statement = select(Book).limit(limit).offset(offset)
        result = await session.execute(statement)

        return result.scalars().all()

    # 2. SIRF EK USER KI BOOKS (Yahan 'where' clause bahut zaroori tha)
    async def get_user_books(self, user_uid: UUID, session: AsyncSession):
        # Database ko bolo: "Wahi books do jahan user_uid match kare"
        statement = select(Book).where(Book.user_uid == user_uid)
        result = await session.execute(statement)
        return result.scalars().all()

    # 3. ID se book dhundhne ke liye
    async def get_book_by_id(self, book_id: str, session: AsyncSession):
        result = await session.execute(
            select(Book).where(Book.id == book_id)
        )
        return result.scalars().one_or_none()

    # 4. Nayi book banane ke liye
    async def create_book(self, data, user_uid: str, session: AsyncSession):
        new_book = Book(**data.model_dump())
        new_book.user_uid = user_uid

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    # 5. Book update karne ke liye
    async def update_book(self, book_id: UUID, data, session: AsyncSession):
        # Yahan humne upar wala get_book_by_id use kiya hai
        book = await self.get_book_by_id(book_id, session)

        if not book:
            return None

        updated_data = data.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(book, key, value)

        book.updated_at = datetime.now()

        await session.commit()
        await session.refresh(book)
        return book

    # 6. Book udaane ke liye
    async def delete_book(self, book_id: UUID, session: AsyncSession):
        book = await self.get_book_by_id(book_id, session)

        if not book:
            return False

        await session.delete(book)
        await session.commit()
        return True