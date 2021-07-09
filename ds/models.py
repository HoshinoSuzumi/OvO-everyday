from sqlalchemy import Column, Text, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from .database import ModelBase


class User(ModelBase):
    __tablename__ = 'users'

    email = Column(Text, primary_key=True)
    name = Column(Text)
    website = Column(Text)


class Comment(ModelBase):
    __tablename__ = 'comments'

    id = Column(Text, primary_key=True)
    content = Column(Text)
    ctime = Column(DateTime)

    domain = Column(Text)
    path = Column(Text)
    # Sender info
    user = Column(JSON)

    children = relationship("Reply", back_populates="comment")


class Reply(ModelBase):
    __tablename__ = 'replies'

    id = Column(Text, primary_key=True)
    content = Column(Text)
    ctime = Column(DateTime)

    domain = Column(Text)
    path = Column(Text)
    # Sender info
    user = Column(JSON)
    # Comment uuid
    cid = Column(Text, ForeignKey('comments.id'))
    comment = relationship("Comment", back_populates="children")
