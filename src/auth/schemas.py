from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List, Optional
from src.books.schemas import BookCreate
from ..reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=7, max_length=72)

class UserModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    hashed_password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    books:List[BookCreate]

class UserBooksModel(UserModel):
    books: List[BookCreate]
    reviews: List[ReviewModel]

class UserLogicModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=7, max_length=72)

