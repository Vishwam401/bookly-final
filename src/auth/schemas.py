from pydantic import BaseModel, Field
import uuid
from datetime import datetime


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

class UserLogicModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=7, max_length=72)

