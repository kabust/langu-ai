import jwt

from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal
from settings import settings
from user.crud import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_db() -> AsyncSession: # type: ignore
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def get_current_user(token: str = Security(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
