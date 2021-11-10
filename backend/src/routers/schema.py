from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserIn(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr


class UserOut(BaseModel):
    id: int
    username: str = Field(min_length=5, max_length=20)
    join_date: datetime
    is_verifide: bool


class PostSort(str, Enum):
    old = 'old'
    new = 'new'
    like = 'like'
