import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    website: str


class UserCreate(UserBase):
    email: str


class User(UserBase):
    class Config:
        orm_mode = True


class ReplyBase(BaseModel):
    content: str
    user: User
    cid: str


class ReplyCreate(ReplyBase):
    user: UserCreate


class Reply(ReplyBase):
    id: str
    ctime: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str
    domain: str
    path: str
    user: User


class CommentCreate(CommentBase):
    user: UserCreate


class Comment(CommentBase):
    id: str
    ctime: Optional[datetime.datetime] = None
    children: List[Reply] = []

    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    done: bool = True
    comments: List[Comment]
