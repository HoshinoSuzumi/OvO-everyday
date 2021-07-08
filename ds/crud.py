import datetime
import urllib.parse

from sqlalchemy.orm import Session

from utils import Utils
from . import models, schemas


def get_comments_count(db: Session):
    return db.query(models.Comment).count()


def get_comments(db: Session, domain: str, path: str, offset: int = 0, limit: int = 10):
    return db.query(models.Comment) \
        .filter(models.Comment.domain == urllib.parse.unquote(domain)) \
        .filter(models.Comment.path == urllib.parse.unquote(path)) \
        .offset(offset).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        id=str(Utils.uuid_unmapped()),
        ctime=datetime.datetime.now(),
        content=Utils.xss_filter(comment.content),
        domain=comment.domain,
        path=comment.path,
        user=dict(comment.user)
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_or_update_user(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    else:
        db_user = db.query(models.User).filter(models.User.email == user.email)
        db_user.update(dict(user))
        db.commit()
        db.refresh(db_user.first())
    return db_user


def create_reply(db: Session, reply: schemas.ReplyCreate):
    db_reply = models.Reply(
        id=str(Utils.uuid_unmapped()),
        ctime=datetime.datetime.now(),
        content=Utils.xss_filter(reply.content),
        user=reply.user,
        cid=reply.cid
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply
