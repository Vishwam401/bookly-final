from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import get_current_user
from src.db.database import get_session
from src.db.models import User
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from src.reviews.service import ReviewService


review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_uid}", response_model=ReviewModel, status_code=status.HTTP_201_CREATED)
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await review_service.add_review_to_book(
        user_email=current_user.email,
        book_id=book_uid,
        review_data=review_data,
        session=session,
    )