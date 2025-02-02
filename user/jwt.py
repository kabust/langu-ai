import jwt

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
