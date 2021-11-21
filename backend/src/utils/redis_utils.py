from datetime import timedelta
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)


def save_password_code(*, r: Redis = redis, email: str, code: int):
    email = f'C_{email}'
    r.set(email, code)
    r.expire(email, int(timedelta(minutes=10).total_seconds()))


def get_password_code(*, r: Redis = redis, email: str):
    email = f'C_{email}'
    code: bytes = r.get(email)
    code = int(code.decode("utf-8"))
    return code


def email_limited(*, r: Redis = redis, email: str):
    email = f'EL_{email}'
    if r.setnx(email, 10):  # add email in db if not exist
        # remove email after 5 minutes (unlimited user)
        r.expire(email, int(timedelta(minutes=5).total_seconds()))

    bucket = r.decrby(email, 1)

    if bucket < 0:  # if user limited
        return True
    return False
