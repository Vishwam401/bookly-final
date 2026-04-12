from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.reviews.schemas import ReviewModel


class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    price: float
    pages: int
    language: str
    rating: float


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    pages: Optional[int] = None
    language: Optional[str] = None
    is_available: Optional[bool] = None


class BookRead(BaseModel):
    id: UUID
    title: str
    author: str
    price: float
    language: str
    created_at: datetime
    updated_at: datetime


class BookDetail(BookRead):
    reviews: List[ReviewModel]