from datetime import timedelta
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)


def save_password_code(*, r: Redis = redis, email: str, code: int):
    r.set(email, code)
    r.expire(email, int(timedelta(minutes=10).total_seconds()))


def get_password_code(*, r: Redis = redis, email: str):
    code: bytes = r.get(email)
    code = int(code.decode("utf-8"))
    return code
