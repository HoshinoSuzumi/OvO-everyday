import datetime
from typing import List, Optional

from pydantic import BaseModel


class ReplyBase(BaseModel):
    content: str
    sender_name: str
    sender_mail: str
    sender_site: str
    attached_to: str


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyBase):
    uuid: str
    create_time: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str
    domain: str
    path: str
    sender_name: str
    sender_mail: str
    sender_site: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    uuid: str
    create_time: Optional[datetime.datetime] = None
    replies: List[Reply] = []

    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    done: bool = True
    comments: List[Comment]
