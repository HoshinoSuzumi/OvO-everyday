import datetime
from sqlalchemy.orm import Session

from utils import Utils
import models
import schemas


def get_comments_count(db: Session):
    return db.query(models.Comment).count()


def get_comments(db: Session, domain: str, path: str, offset: int = 0, limit: int = 10):
    return db.query(models.Comment) \
        .filter(models.Comment.domain == domain) \
        .filter(models.Comment.path == path) \
        .offset(offset).limit(limit).all()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        uuid=str(Utils.uuid_unmapped()),
        content=comment.content,
        domain=comment.domain,
        path=comment.path,
        create_time=datetime.datetime.now(),
        sender_name=comment.sender_name,
        sender_mail=comment.sender_mail,
        sender_site=comment.sender_site
    )
    db.add(db_comment)
    db.commit()
