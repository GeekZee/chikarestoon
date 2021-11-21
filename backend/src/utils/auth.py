from datetime import datetime, timedelta
import time

from ..db.models import User
from ..db.database import engine
from .config import get_settings
from .redis_utils import is_token_invalid_in_redis, save_expire_token

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="v1/token")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, database_hashed_password):
    return pwd_context.verify(plain_password, database_hashed_password)


async def authenticate_user(username: str, password: str):
    async with AsyncSession(engine) as session:
        user = await session.exec(select(User).where(
            User.username == username))
        user = user.first()

    if user and verify_password(password, user.password):
        return user
    return False


async def token_generator(username: str, password: str, ):
    user = await authenticate_user(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_expire = datetime.utcnow() + timedelta(minutes=15)
    refresh_expire = datetime.utcnow() + timedelta(days=1)

    access_token_data = {
        "uid": user.id,
        "typ": "A",  # access_token
        "exp": access_expire}

    refresh_token_data = {
        "uid": user.id,
        "typ": "R",  # refresh_token
        "exp": refresh_expire}

    access_token = jwt.encode(access_token_data,
                              get_settings().SECRET,
                              algorithm="HS256")

    refresh_token = jwt.encode(refresh_token_data,
                               get_settings().SECRET,
                               algorithm="HS256")

    return {"token_type": "bearer", 'access_token': access_token, 'refresh_token': refresh_token}


async def token_generator_by_refresh_token(user: User):
    access_expire = datetime.utcnow() + timedelta(minutes=15)

    access_token_data = {
        "uid": user.id,
        "typ": "A",  # access_token
        "exp": access_expire}

    access_token = jwt.encode(access_token_data,
                              get_settings().SECRET,
                              algorithm="HS256")

    return {"token_type": "bearer", 'access_token': access_token}


async def get_current_user_by_refresh_token(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, get_settings().SECRET,
                             algorithms=["HS256"])
    except:
        raise credentials_exception
    try:
        if payload['typ'] == 'R':  # refresh_token
            user_id = payload['uid']

            if is_token_invalid_in_redis(user_id=user_id, token=token):
                raise credentials_exception

            async with AsyncSession(engine) as session:
                user = await session.exec(select(User).where(
                    User.id == user_id))
                user = user.first()
            if user:
                return user

        raise credentials_exception
    except:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, get_settings().SECRET,
                             algorithms=["HS256"])
    except:
        raise credentials_exception

    try:

        if payload['typ'] == 'A':  # access_token
            user_id = payload['uid']

            if is_token_invalid_in_redis(user_id=user_id, token=token):
                raise credentials_exception

            async with AsyncSession(engine) as session:
                user = await session.exec(select(User).where(
                    User.id == user_id))
                user = user.first()
            if user:
                return user

        raise credentials_exception
    except:
        raise credentials_exception


def expired_token(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(token, get_settings().SECRET,
                         algorithms=["HS256"])
    try:
        uid = payload['uid']
        exp = int(payload['exp'] - time.time()) + 10

        save_expire_token(user_id=uid, token=token, expire_secound=exp)
    except:
        raise credentials_exception
