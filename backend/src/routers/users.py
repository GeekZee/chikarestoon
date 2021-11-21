from random import randint


from ..db.models import User
from ..utils.redis_utils import get_password_code, save_password_code
from ..db.database import engine
from ..utils.email import send_email_verification_mail, send_email_change_password
from ..utils.config import get_settings
from ..utils.auth import (verify_password,
                          get_hashed_password,
                          token_generator,
                          token_generator_by_refresh_token,
                          get_current_user,
                          get_current_user_by_refresh_token,
                          expired_token)

from .schema import (UserIn,
                     UserUpdate,
                     UserOut,
                     UserOutPrivateData,
                     AccessRefreshToken,
                     RefreshToken,
                     ChangePasswordByEmail,
                     ChangePassword,
                     )


from fastapi import (Depends,
                     APIRouter,
                     HTTPException,
                     status,
                     Request,
                     Body
                     )
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from pydantic import EmailStr

import jwt


router = APIRouter()

template = Jinja2Templates(directory="templates")


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


@router.post("/user/", response_model=UserOutPrivateData, status_code=status.HTTP_201_CREATED, tags=['user'])
async def create_user(*, session: Session = Depends(get_session), user: UserIn):

    email_in_db = await session.exec(select(User).where(User.email == user.email))
    if email_in_db.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    username_in_db = await session.exec(select(User).where(User.username == user.username))
    if username_in_db.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user.password = get_hashed_password(user.password)
    db_user = User.from_orm(user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    await send_email_verification_mail(db_user.email, db_user)
    return db_user


@router.put('/user/', response_model=UserOutPrivateData, status_code=status.HTTP_202_ACCEPTED, tags=['user'])
async def update_user(user_new_data: UserUpdate,
                      user: User = Depends(get_current_user),
                      session: Session = Depends(get_session)
                      ):

    if user_new_data.username != user.username:
        username_in_db = await session.exec(select(User).where(User.username == user_new_data.username))
        if username_in_db.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        user.username = user_new_data.username

    if user_new_data.email != user.email:
        email_in_db = await session.exec(select(User).where(User.email == user_new_data.email))
        if email_in_db.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        user.is_verifide = False
        user.email = user_new_data.email
        await send_email_verification_mail(user.email, user)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.delete('/user/', status_code=status.HTTP_204_NO_CONTENT, tags=['user'])
async def delete_user(user: User = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    session.delete(user)
    await session.commit()


@router.get('/user/me', response_model=UserOutPrivateData, tags=['user'])
async def full_user_profile(user: User = Depends(get_current_user)):
    return user


@router.get('/user/{username}', response_model=UserOut, tags=['user'])
async def user_public_data(username: str, session: Session = Depends(get_session)):
    user = await session.exec(select(User).where(User.username == username))
    user = user.first()
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Username Not Found"
    )


@router.post('/users/verification/email', tags=['email'], status_code=status.HTTP_204_NO_CONTENT)
async def send_new_email_verification(user: User = Depends(get_current_user)):
    await send_email_verification_mail(user.email, user)


@router.get("/users/verification/email", response_class=HTMLResponse, tags=['email'])
async def email_verification(request: Request,
                             token: str,
                             session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token,
                             get_settings().SECRET,
                             algorithms=["HS256"])

        if payload.get("typ") == 'E':  # Email
            user = await session.exec(
                select(User).where(User.id == payload.get("uid")))
            user = user.first()

            if user:
                if not user.is_verifide:
                    user.is_verifide = True
                    session.add(user)
                    await session.commit()
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


@router.post("/token", response_model=AccessRefreshToken, tags=['token'])
async def generate_access_token_and_refresh_token(request_form: OAuth2PasswordRequestForm = Depends()):
    return await token_generator(request_form.username, request_form.password)


@router.post('/token/verify', tags=['token'], status_code=status.HTTP_204_NO_CONTENT)
async def is_token_valid(user: User = Depends(get_current_user)):
    '''Takes a `access_token` and if it is valid, return a `HTTP 204 NO CONTENT` and if it not valid return `HTTP 401 Unauthorized`
    '''


@router.post('/token/refresh', response_model=RefreshToken, tags=['token'])
async def fresh_access_token(user: User = Depends(get_current_user_by_refresh_token)):
    '''get a `refresh_token` and return a new`access_token`'''
    return await token_generator_by_refresh_token(user)


@router.post('/token/expire', status_code=status.HTTP_204_NO_CONTENT, tags=['token'])
async def expire_token_and_logout_user(token: None = Depends(expired_token)):
    pass


@router.post('/password/reset/', tags=['password'], status_code=status.HTTP_204_NO_CONTENT)
async def forget_password_send_code(email: EmailStr, session: Session = Depends(get_session)):
    '''get a email and sends a 6-digit recovery code'''
    user = await session.exec(select(User).where(User.email == email))
    user = user.first()
    if user:
        code = randint(100000, 999999)

        save_password_code(email=email, code=code)

        await send_email_change_password(code, email, user)
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@router.put('/password/reset/confirm/', tags=['password'], status_code=status.HTTP_204_NO_CONTENT)
async def confirm_reset_code_and_new_password(data: ChangePasswordByEmail, session: Session = Depends(get_session)):
    code_on_db = get_password_code(email=data.email)

    if code_on_db and data.code == code_on_db:
        user = await session.exec(
            select(User).where(User.email == data.email))
        user = user.first()

        if user:
            user.password = get_hashed_password(data.new_password)
            session.add(user)
            await session.commit()
            return

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect code")


@router.put('/password/change/', tags=['password'], status_code=status.HTTP_204_NO_CONTENT)
async def change_password(data: ChangePassword,
                          user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):

    db_user_password = user.password
    if verify_password(data.old_password, db_user_password):
        user.password = get_hashed_password(data.new_password)
        session.add(user)
        await session.commit()

    # TODO When the password is changed -> logout user
