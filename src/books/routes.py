from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.books.schemas import BookCreate, BookUpdate
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database import engine
from sqlmodel import select
from src.books.models import Book


books_router = APIRouter(prefix="/books", tags=["books"])
service = BookService()

async def get_session():
    async with AsyncSession(engine) as session:
        yield session


# GET ALL + PAGINATION
@books_router.get("/")
async def get_book(
        limit: int = 10,
        offset: int = 0,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Book).offset(offset).limit(limit)
    )
    return result.scalars().all()

@books_router.get("/search")
async def search_books(
        min_price: float = 0,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Book).where(Book.price >= min_price)

    )
    return result.scalars().all()

# GET BY ID

@books_router.get("/{book_id}")
async def get_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book = await service.get_book(book_id, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# CREATE
@books_router.post("/")
async def create_book(
        data: BookCreate,
        session: AsyncSession = Depends(get_session)
):
    return await service.create_book(data, session)

# UPDATE
@books_router.put("/{book_id}")
async def update_book(
        book_id: UUID,
        data: BookUpdate,
        session: AsyncSession = Depends(get_session)
):
    book = await service.update_book(book_id, data, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# DELETE

@books_router.delete("/{book_id}")
async def delete_book(
        book_id: UUID,
        session: AsyncSession = Depends(get_session)
):
    success = await service.delete_book(book_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


# FILTER



















