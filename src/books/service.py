from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Book
from src.books.schemas import BookCreate, BookUpdate


class BookService:
    async def get_all_books(self, limit: int, offset: int, session: AsyncSession):
        result = await session.execute(select(Book).limit(limit).offset(offset))
        return result.scalars().all()

    async def get_user_books(self, user_uid: UUID, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.user_uid == user_uid))
        return result.scalars().all()

    async def get_book_by_id(self, book_id: str, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.id == book_id))
        return result.scalars().one_or_none()

    async def search_books(self, min_price: float, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.price >= min_price))
        return result.scalars().all()

    async def create_book(self, data: BookCreate, user_uid: str, session: AsyncSession) -> Book:
        new_book = Book(**data.model_dump(), user_uid=user_uid)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_id: UUID, data: BookUpdate, session: AsyncSession):
        book = await self.get_book_by_id(book_id, session)

        if not book:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)

        book.updated_at = datetime.now()
        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_id: UUID, session: AsyncSession) -> bool:
        book = await self.get_book_by_id(book_id, session)

        if not book:
            return False

        await session.delete(book)
        await session.commit()
        return True