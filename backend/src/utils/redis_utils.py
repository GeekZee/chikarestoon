from .config import get_settings

from datetime import timedelta
from redis import Redis

from fastapi import HTTPException, status
import jwt


redis = Redis(host='localhost', port=6379, db=0)


def save_password_code(*, r: Redis = redis, email: str, code: int) -> None:
    email = f'C_{email}'
    r.set(email, code)
    r.expire(email, int(timedelta(minutes=10).total_seconds()))


def get_password_code(*, r: Redis = redis, email: str) -> int:
    email = f'C_{email}'
    code: bytes = r.get(email)
    code = int(code.decode("utf-8"))
    return code


def email_limited(*, r: Redis = redis, email: str) -> bool:
    email = f'EL_{email}'
    if r.setnx(email, 10):  # add email in db if not exist
        # remove email after 5 minutes (unlimited user)
        r.expire(email, int(timedelta(minutes=5).total_seconds()))

    bucket = r.decrby(email, 1)

    if bucket < 0:  # if user limited
        return True
    return False


def save_expire_token(*, r: Redis = redis, user_id: int, token: str, expire_secound: int) -> None:
    if r.setnx(f'{user_id}_{token}', 'exp'):
        r.expire(token, expire_secound)


def is_token_invalid_in_redis(*, r: Redis = redis, user_id: int, token: str) -> bool:
    if r.exists(f'{user_id}_{token}'):
        return True
    return False
