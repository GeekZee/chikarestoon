from .db.models import Hashtag, User, Post
from .db.database import create_db_and_tables, engine

from fastapi import FastAPI
from sqlmodel import Session


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(title="chikarestoon")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
