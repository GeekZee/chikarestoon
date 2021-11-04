from typing import List, Optional
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint
from pydantic import EmailStr


class UserPostLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", primary_key=True
    )


class PostHashtagLink(SQLModel, table=True):
    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", primary_key=True
    )
    hashtag_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


class UserBase(SQLModel):
    pass


class User(UserBase, table=True):
    __table_args__ = (UniqueConstraint("username"), UniqueConstraint("email"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr
    join_date: datetime = Field(default=datetime.utcnow)
    is_super_user: bool = Field(default=False)
    is_verifide: bool = Field(default=False)
    posts: List["Post"] = Relationship(back_populates="user")
    favorites: List["Post"] = Relationship(
        back_populates="likes", link_model=UserPostLink)


class UserCreateUpdate(UserBase):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr


class UserRead(UserBase):
    id: int


class PostBase(SQLModel):
    title: str = Field(min_length=10, max_length=50)
    description: str = Field(min_length=10, max_length=1000)


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")
    likes: List[User] = Relationship(
        back_populates="favorites", link_model=UserPostLink)
    hashtags: List["Hashtag"] = Relationship(
        back_populates="posts", link_model=PostHashtagLink)


class PostCreate(PostBase):
    hashtags: List[str]


class PostUpdate(PostBase):
    hashtags: List[str]


class PostRead(PostBase):
    id: int


class Hashtag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashtag_name: str = Field(min_length=1)
    posts: List[Post] = Relationship(
        back_populates="hashtags", link_model=PostHashtagLink)
