import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__= 'users'
    uid : uuid.UUID = Field(
            default_factory=uuid.uuid4,
            nullable=False,
            primary_key=True

    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    hashed_password: str = Field(exclude=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    def __repr__(self):
        return f'<User {self.username}>'



