from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime


class UserBase(SQLModel):
    pass


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr
    join_date: datetime = Field(default=datetime.utcnow)
    is_super_user: bool = Field(default=False)
    is_verifide: bool = Field(default=False)
    posts: List["Post"] = Relationship(back_populates="author")
    user_likes: List["Post"] = Relationship(back_populates="likes")


class UserCreateUpdate(UserBase):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr


class UserRead(UserBase):
    id: int


class PostBase(UserBase):
    title: str = Field(min_length=10, max_length=200)
    description: str = Field(min_length=10, max_length=1000)


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: User = Relationship(back_populates="posts")
    likes: List[User] = Relationship(back_populates="user_likes")
    hashtags: List["Hashtag"] = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostRead(PostBase):
    id: int


class Hashtag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashtag_name: str = Field(min_length=1)
    posts: List[Post] = Relationship(back_populates="hashtag")
