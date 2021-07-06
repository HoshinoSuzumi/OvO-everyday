import datetime
from typing import List, Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    domain: str
    path: str
    create_time: Optional[datetime.datetime] = None
    sender_name: str
    sender_mail: str
    sender_site: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    uuid: str

    class Config:
        orm_mode = True


class ReplyBase(BaseModel):
    uuid: str


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyBase):
    content: str
    create_time: str
    sender_name: str
    sender_mail: str
    sender_site: str
    attached_to: str

    class Config:
        orm_mode = True
