from sqlmodel import select
from src.books.models import Book
from datetime import datetime


class BookService:

    async def get_book(self, session):
        result = await session.execute(select(Book))
        return result.scalars().all()


    async def get_book(self, book_id, session):
        result = await session.execute(
            select(Book).where(Book.id == book_id)
        )
        return result.scalars().one_or_none()

    async def create_book(self, data, session):
        new_book = Book(**data.model_dump())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_id, data, session):
        book = await self.get_book(book_id, session)
        if not book:
            return None

        updated_book = data.model_dump(exclude_unset=True)

        for key, value in updated_book.items():
            setattr(book, key, value)

        book.updated_at = datetime.now()

        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_id, session):
        book = await self.get_book(book_id, session)
        if not book:
            return False

        await session.delete(book)
        await session.commit()
        return True
