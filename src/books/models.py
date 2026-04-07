from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime



class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    title: str
    author: str
    description: str | None = None

    price: float
    rating: float
    pages: int

    language: str
    is_available: bool = True

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)