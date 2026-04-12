from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.books.schemas import BookCreate, BookDetail, BookUpdate
from src.books.service import BookService
from src.db.database import get_session


books_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker_all = Depends(RoleChecker(allowed_roles=["admin", "user"]))
role_checker_admin = Depends(RoleChecker(allowed_roles=["admin"]))


@books_router.get("/", response_model=List[BookDetail], dependencies=[role_checker_all])
async def get_all_books(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    return await book_service.get_all_books(limit, offset, session)


@books_router.get("/user/{user_uid}", response_model=List[BookDetail], dependencies=[role_checker_all])
async def get_user_books(
    user_uid: UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    return await book_service.get_user_books(user_uid, session)


@books_router.get("/search", response_model=List[BookDetail], dependencies=[role_checker_admin])
async def search_books(
    min_price: float = 0,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    return await book_service.search_books(min_price, session)


@books_router.get("/{book_id}", response_model=BookDetail, dependencies=[role_checker_all])
async def get_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.get_book_by_id(book_id, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@books_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[role_checker_all])
async def create_book(
    data: BookCreate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    user_uid = token_details.get("user", {}).get("user_uid")
    return await book_service.create_book(data, user_uid, session)


@books_router.put("/{book_id}", dependencies=[role_checker_all])
async def update_book(
    book_id: UUID,
    data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.update_book(book_id, data, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker_admin])
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    success = await book_service.delete_book(book_id, session)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")