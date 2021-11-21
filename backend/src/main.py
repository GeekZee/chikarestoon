from .db.models import Hashtag, User, Post, UserPostLikeLink, PostHashtagLink
from .db.database import create_db_and_tables, engine
from .routers import users

from fastapi import FastAPI


app = FastAPI(title="chikarestoon")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(users.router, prefix='/v1')
