import jwt

from fastapi import HTTPException, Request, Security, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal
from settings import settings
from user.crud import get_user_by_email


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_db() -> AsyncSession: # type: ignore
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def get_current_user_email(request: Request) -> str:
    token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
