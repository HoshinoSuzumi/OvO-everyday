import datetime
import json
import urllib.parse

from sqlalchemy.orm import Session

from utils import Utils
import models
import schemas


def get_comments_count(db: Session):
    return db.query(models.Comment).count()


def get_comments(db: Session, domain: str, path: str, offset: int = 0, limit: int = 10):
    return db.query(models.Comment) \
        .filter(models.Comment.domain == urllib.parse.unquote(domain)) \
        .filter(models.Comment.path == urllib.parse.unquote(path)) \
        .offset(offset).limit(limit).all()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        id=str(Utils.uuid_unmapped()),
        content=comment.content,
        domain=comment.domain,
        path=comment.path,
        ctime=datetime.datetime.now(),
        user=dict(comment.user)
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_reply(db: Session, reply: schemas.ReplyCreate):
    db_reply = models.Reply(
        **reply.dict(),
        id=str(Utils.uuid_unmapped()),
        ctime=datetime.datetime.now()
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply
