from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from .schemas import BookCreate, BookUpdate, BookRead, BookDetail as BookModel, BookDetail
from .service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database import get_session # Seedha get_session use karo
from src.auth.dependencies import AccessTokenBearer, RoleChecker


books_router = APIRouter(prefix="/books", tags=["books"])
service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker_all = Depends(RoleChecker(['admin', 'user']))
role_checker_admin = Depends(RoleChecker(['admin']))

# GET ALL BOOKS
@books_router.get("/", response_model=List[BookModel], dependencies=[role_checker_all])
async def get_all_books(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    return await service.get_all_books(limit, offset, session)

# GET BOOKS BY SPECIFIC USER (THE ONE YOU ASKED FOR)
@books_router.get("/user/{user_uid}", response_model=List[BookModel], dependencies=[role_checker_all])
async def get_user_book_submission(
    user_uid: UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    # Service se filter karwayenge user_uid ke basis pe
    return await service.get_user_books(user_uid, session)

# SEARCH BOOKS (ADMIN ONLY)
@books_router.get("/search", response_model=List[BookModel], dependencies=[role_checker_admin])
async def search_books(
    min_price: float = 0,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    return await service.search_books(min_price, session)

# GET BOOK BY ID
@books_router.get("/{book_id}", response_model=BookDetail, dependencies=[role_checker_all])
async def get_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    print("------ ROUTE HIT HO GAYA! ------")
    book = await service.get_book_by_id(book_id, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

# CREATE BOOK
@books_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[role_checker_all])
async def create_book(
    data: BookCreate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    # Dhyan rakhna token mein 'user_id' hai ya 'user_uid'
    user_id = token_details.get('user')['user_uid']
    return await service.create_book(data, user_id, session)

# UPDATE BOOK
@books_router.put("/{book_id}", dependencies=[role_checker_all])
async def update_book(
    book_id: UUID,
    data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    book = await service.update_book(book_id, data, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# DELETE BOOK
@books_router.delete("/{book_id}", dependencies=[role_checker_admin]) # Delete admin ko de diya
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    success = await service.delete_book(book_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}