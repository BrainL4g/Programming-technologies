import random, string, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from backend.src.core.config import settings
from backend.src.exceptions import InvalidToken, TokenExpired
from backend.src.db.redis_client.service import redis_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str | Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_EXP)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return encoded_jwt


# def create_refresh_token(subject: str | Any) -> str:
#     expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_REFRESH_EXP)
#     to_encode = {"exp": expire, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
#     return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def verify_token(token: str) -> Union[str, Any]:
    if await redis_service.is_token_blacklisted(token):
        raise InvalidToken()
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=settings.JWT_ALG
        )
        return decoded_token["sub"]
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except jwt.InvalidTokenError:
        raise InvalidToken()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_random_code() -> str:
    return "".join(random.choices(string.digits, k=6))
