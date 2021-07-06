import json
from typing import List
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, DATABASE_ENGINE
from utils import Utils

models.ModelBase.metadata.create_all(bind=DATABASE_ENGINE)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {
        'message': 'Welcome to OvO server',
        'api-document': '/docs'
    }


@app.get('/comment', response_model=schemas.CommentResponse)
def read_comment(domain: str, path: str, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comments = crud.get_comments(db=db, domain=domain, path=path, offset=offset, limit=limit)
    return {
        'done': Utils.is_fetch_done(crud.get_comments_count(db), offset, limit),
        'comments': comments
    }


@app.post('/comment', response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)
