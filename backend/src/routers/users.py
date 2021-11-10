

from ..db.models import User
from .schema import UserIn, UserOut
from ..db.database import engine
from ..utils.passwd import get_hashed_password, verify_password
from ..utils.email import send_mail
from ..utils.config import get_settings

from fastapi import (Depends,
                     APIRouter,
                     HTTPException,
                     status,
                     Request,
                     )
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select
import jwt

router = APIRouter()

template = Jinja2Templates(directory="templates")


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/signup/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def sign_up(*, session: Session = Depends(get_session), user: UserIn):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user.password = get_hashed_password(user.password)
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    await send_mail([db_user.email], db_user)
    return db_user


@router.get("/verification/email", response_class=HTMLResponse)
async def email_verification(request: Request,
                             token: str,
                             session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token,
                             get_settings().SECRET,
                             algorithms=["HS256"])

        if payload.get("type") == 'email_verification':
            user = session.exec(
                select(User).where(User.id == payload.get("id"))).first()

            if user:
                if not user.is_verifide:
                    user.is_verifide = True
                    session.add(user)
                    session.commit()
                context = {
                    "request": request,
                    "username": user.username,
                    "is_verifide": f'تایید ایمیل با موفقیت انجام شد'}
                return template.TemplateResponse("verification.html", context)

        context = {
            "request": request,
            "is_verifide": 'اکانت یافت نشد'
        }
        return template.TemplateResponse("verification.html", context)

    except:
        context = {
            "request": request,
            "is_verifide": 'اکانت یافت نشد'
        }
        return template.TemplateResponse("verification.html", context)


@router.get('/{username}', response_model=UserOut)
async def user(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Username Not Found"
    )
