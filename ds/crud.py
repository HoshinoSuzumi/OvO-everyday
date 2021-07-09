import datetime
import urllib.parse
import asyncio

from sqlalchemy.orm import Session

from lib.utils import Utils
from config.mail import Template
from . import models, schemas

Utils = Utils()


def _mail_mention(db: Session, model: [schemas.Comment, schemas.Reply]):
    for user in get_users_from_message(db=db, message=model.content):
        asyncio.run(Utils.get_mailer().send(
            mailto=user.email,
            subject='有人在评论中提到您！',
            fields={
                'content': model.content,
                'domain': model.domain,
                'path': model.path
            },
            template=Template.TEMPLATE_MENTION
        ))


def _mail_reply(db: Session, reply: schemas.Reply):
    asyncio.run(Utils.get_mailer().send(
        mailto=get_user_by_name(db, get_comment_by_id(db, reply.cid).user['name']).email,
        subject='评论收到新的回复！',
        fields={
            'content': reply.content,
            'domain': reply.domain,
            'path': reply.path
        },
        template=Template.TEMPLATE_REPLY
    ))


def get_comments_count(db: Session):
    return db.query(models.Comment).count()


def get_comments(db: Session, domain: str, path: str, offset: int = 0, limit: int = 10):
    return db.query(models.Comment) \
        .filter(models.Comment.domain == urllib.parse.unquote(domain)) \
        .filter(models.Comment.path == urllib.parse.unquote(path)) \
        .offset(offset).limit(limit).all()


def get_comment_by_id(db: Session, uuid: str) -> schemas.Comment:
    return db.query(models.Comment).filter(models.Comment.id == uuid).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users_from_message(db: Session, message: str) -> list[schemas.UserCreate]:
    username_list = []
    valid_users = []
    message = message.split(' ')
    for username in message:
        username = username[username.find('@') + 1:].strip('\n')
        if username != '' and username not in username_list:
            username_list.append(username)
            user = get_user_by_name(db, username)
            if user is not None:
                valid_users.append(user)
    return valid_users


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
    _mail_mention(db, db_comment)
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
        domain=reply.domain,
        path=reply.path,
        user=dict(reply.user),
        cid=reply.cid
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    _mail_reply(db, db_reply)
    _mail_mention(db, db_reply)
    return db_reply
