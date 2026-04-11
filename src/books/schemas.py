from pydantic import BaseModel
from datetime import datetime
from ..reviews.schemas import ReviewModel
from uuid import UUID
from typing import List

class BookCreate(BaseModel):
    title: str
    author: str
    description: str | None = None
    price: float
    pages: int
    language: str
    rating: float


class BookUpdate(BaseModel):
     title: str | None = None
     author: str | None = None
     description: str | None = None
     price: float | None = None
     rating: float | None = None
     pages: int | None = None
     language: str | None = None
     is_available: bool | None = None

class BookRead(BaseModel):
    id: UUID
    title: str
    author: str
    price: float
    language: str
    created_at: datetime
    updated_at: datetime

class  BookDetail(BookRead):
    reviews: List[ReviewModel]