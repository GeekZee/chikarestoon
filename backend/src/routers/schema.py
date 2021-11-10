from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class RefreshToken(BaseModel):
    access_token: str
    token_type: str


class AccessRefreshToken(RefreshToken):
    refresh_token: str


class UserIn(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr


class UserOut(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    join_date: datetime
    is_verifide: bool


class UserOutPrivateData(UserOut):
    id: int
    email: EmailStr
    is_super_user: bool


class PostSort(str, Enum):
    old = 'old'
    new = 'new'
    like = 'like'
