import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.reviews.schemas import ReviewModel

class TagCreateModel(BaseModel):
    name: str

class TagModel(BaseModel):
    id: uuid.UUID
    name: str

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    price: float
    pages: int
    language: str
    rating: float
    tag_names: Optional[List[str]] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    pages: Optional[int] = None
    language: Optional[str] = None
    is_available: Optional[bool] = None
    tag_names: Optional[List[str]] = None


class BookRead(BaseModel):
    id: UUID
    title: str
    author: str
    price: float
    language: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagModel]


class BookDetail(BookRead):
    reviews: List[ReviewModel]