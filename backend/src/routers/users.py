from ..db.models import User, UserIn, UserOut
from ..db.database import engine
from ..utils.passwd import get_hashed_password, verify_password
from ..utils.email import send_mail

from fastapi import Depends, APIRouter, HTTPException, Query
from sqlmodel import Session


router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/signup/", response_model=UserOut)
async def sign_up(*, session: Session = Depends(get_session), user: UserIn):
    user.password = get_hashed_password(user.password)
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    await send_mail([db_user.email], db_user)
    return db_user
