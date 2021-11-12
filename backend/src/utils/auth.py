from datetime import datetime, timedelta


from ..db.models import User
from ..db.database import engine
from ..utils.config import get_settings

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, database_hashed_password):
    return pwd_context.verify(plain_password, database_hashed_password)


async def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.username == username)).first()

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
        "user_id": user.id,
        "type": "access_token",
        "exp": access_expire}

    refresh_token_data = {
        "user_id": user.id,
        "type": "refresh_token",
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
        "user_id": user.id,
        "type": "access_token",
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
        if payload['type'] == 'refresh_token':
            user_id = payload['user_id']

            with Session(engine) as session:
                user = session.exec(select(User).where(
                    User.id == user_id)).first()
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
        if payload['type'] == 'access_token':
            user_id = payload['user_id']

            with Session(engine) as session:
                user = session.exec(select(User).where(
                    User.id == user_id)).first()
            if user:
                return user

        raise credentials_exception
    except:
        raise credentials_exception
