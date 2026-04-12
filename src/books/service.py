from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Book, Tag
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

        # 1. Book ka data dict mein convert karo, lekin tags ko alag nikaal lo
        book_dict = data.model_dump()
        tag_names = book_dict.pop("tag_names", [])

        #2. New book ka object banaya
        new_book = Book(**book_dict)
        new_book.user_uid = user_uid

        #3. TAGS LOGIC: har tag name ke liye check kro
        if tag_names:
            for name in tag_names:
                # check kro kya ye tag DB mai pehele se hai?
                statement = select(Tag).where(Tag.name == name)
                result = await session.execute(statement)
                tag = result.scalars().one_or_none()

                #Agar tag nahi mila, toh new Tag banao
                if not tag:
                    tag = Tag(name=name)

                #Book ki 'tags' list mai append kro (M2M link)
                new_book.tags.append(tag)

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book


    async def get_all_tags(self, session: AsyncSession):
        statement = select(Tag)
        result = await session.execute(statement)
        return result.scalars().all()

    async def add_tag_to_book(self, book_id:str, tag_name:str, session: AsyncSession):
        #ek existing book mai baad mai tag add krne ke liye
        book = await self.get_book_by_id(book_id, session)
        if not book:
            return None

        #Tag check/create logic
        statement = select(Tag).where(Tag.name == tag_name)
        result = await session.execute(statement)
        tag = result.scalars().one_or_none()

        if not tag:
            tag = Tag(name=tag_name)

        #check if tag pehele se toh append nai hai
        if tag not in book.tags:
            book.tags.append(tag)
            await session.commit()
            await session.refresh(book)

        return book


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

    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        #check if tags exists or not
        statement = select(Tag).where(Tag.name == tag_uid)
        result = await session.execute(statement)
        tag = result.scalars().one_or_none()

        if not tag:
            return None #tag nai mila huh

        #delete tag
        await session.delete(tag)
        await session.commit()

        return True
