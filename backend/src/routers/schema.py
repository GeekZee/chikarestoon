from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class RefreshToken(BaseModel):
    token_type: str
    access_token: str


class AccessRefreshToken(RefreshToken):
    refresh_token: str


class UserIn(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr


class UserUpdate(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr


class UserOut(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    join_date: datetime
    is_verifide: bool


class UserOutPrivateData(UserOut):
    is_super_user: bool
    email: EmailStr
    id: int


class ChangePassword(BaseModel):
    email: EmailStr
    code: int = Field(ge=100000, le=999999)
    new_password: str = Field(min_length=8)


class PostSort(str, Enum):
    old = 'old'
    new = 'new'
    like = 'like'
