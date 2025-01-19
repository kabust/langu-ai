import hashlib

from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from user import models, schemas


async def get_all_users(db: AsyncSession):
    query = select(models.DBUser)
    users = await db.execute(query)
    return users.fetchall()


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(models.DBUser).where(models.DBUser.id == user_id)
    user = await db.execute(query)
    user = user.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(models.DBUser).where(models.DBUser.email == email)
    user = await db.execute(query)
    user = user.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    user.password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
    query = insert(models.DBUser).values(**user.dict())
    result = await db.execute(query)
    await db.commit()
    response = ...
