import uuid
from datetime import datetime
from typing import List, Optional

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel


class BookTag(SQLModel, table=True):
    __tablename__ = "book_tags"

    book_id: uuid.UUID = Field(foreign_key="books.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tags.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column=Column(pg.VARCHAR, unique=True))

    books: List["Book"] = Relationship(
        back_populates="tags",
        link_model=BookTag
    )


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    author: str
    description: Optional[str] = None
    price: float
    rating: float
    pages: int
    language: str
    is_available: bool = True

    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    tags: List["Tag"] = Relationship(
        back_populates="books",
        link_model=BookTag,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


    def __repr__(self):
        return f"<Book {self.title}>"


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    hashed_password: str = Field(exclude=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    books: List["Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    reviews: List["Review"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    rating: int = Field(lt=5)
    review_text: str

    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"


