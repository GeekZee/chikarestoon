from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint
from pydantic import EmailStr


class UserPostLikeLink(SQLModel, table=True):
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
        default=None, foreign_key="hashtag.id", primary_key=True
    )


class PostUserReportLink(SQLModel, table=True):
    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("username"), UniqueConstraint("email"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr
    join_date: datetime = Field(default=datetime.utcnow())
    is_super_user: bool = Field(default=False)
    is_verifide: bool = Field(default=False)
    posts: List["Post"] = Relationship(back_populates="user")
    favorites: List["Post"] = Relationship(
        back_populates="likes", link_model=UserPostLikeLink)

    reported: List["Post"] = Relationship(
        back_populates="reports", link_model=UserPostLikeLink)


class UserIn(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)
    email: EmailStr


class UserOut(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr
    join_date: datetime
    is_super_user: bool
    is_verifide: bool


class PostBase(SQLModel):
    title: str = Field(min_length=10, max_length=50)
    description: str = Field(min_length=10, max_length=1000)


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")
    likes: List[User] = Relationship(
        back_populates="favorites", link_model=UserPostLikeLink)
    hashtags: List["Hashtag"] = Relationship(
        back_populates="posts", link_model=PostHashtagLink)

    reports: List[User] = Relationship(
        back_populates="reported", link_model=UserPostLikeLink)


class Hashtag(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("hashtag_name"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    hashtag_name: str = Field(min_length=1)
    posts: List[Post] = Relationship(
        back_populates="hashtags", link_model=PostHashtagLink)
