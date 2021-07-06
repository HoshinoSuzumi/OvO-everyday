from sqlalchemy import Column, Text, DateTime
# from sqlalchemy.orm import relationship

from database import ModelBase


class Comment(ModelBase):
    __tablename__ = 'comments'

    uuid = Column(Text, primary_key=True)
    content = Column(Text)
    create_time = Column(DateTime)

    domain = Column(Text)
    path = Column(Text)
    # Sender info
    sender_name = Column(Text)
    sender_mail = Column(Text)
    sender_site = Column(Text)


class Reply(ModelBase):
    __tablename__ = 'replies'

    uuid = Column(Text, primary_key=True)
    content = Column(Text)
    create_time = Column(DateTime)
    # Sender info
    sender_name = Column(Text)
    sender_mail = Column(Text)
    sender_site = Column(Text)
    # Comment uuid
    attached_to = Column(Text)
