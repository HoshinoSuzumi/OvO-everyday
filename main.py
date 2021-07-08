import json
from typing import List
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from ds import *
from utils import Utils

models.ModelBase.metadata.create_all(bind=database.DATABASE_ENGINE)

app = FastAPI()

# CORS Settings
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Documents config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="OvO Everyday",
        version="1.0.1",
        description="Have a nice day!",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware('http')
async def domain_verify(req: Request, call_next):
    print('Middleware #1 ', req.headers['host'])
    res = await call_next(req)
    return res


@app.get('/')
async def root():
    return {
        'message': 'Welcome to OvO server',
        'api-document': '/docs'
    }


@app.get('/comment', response_model=schemas.CommentResponse)
def read_comment(domain: str, path: str, page: int = 0, db: Session = Depends(get_db)):
    comments = crud.get_comments(db=db, domain=domain, path=path, offset=page * 10)
    return {
        'done': Utils.is_fetch_done(crud.get_comments_count(db), page * 10, 10),
        'comments': comments
    }


@app.post('/comment', response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    crud.create_or_update_user(db, comment.user)
    return crud.create_comment(db=db, comment=comment)


@app.post('/reply', response_model=schemas.Reply)
def create_reply(reply: schemas.ReplyCreate, db: Session = Depends(get_db)):
    return crud.create_reply(db=db, reply=reply)
