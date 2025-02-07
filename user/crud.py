import hashlib

from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from user import models, schemas


async def get_all_users(db: AsyncSession) -> models.DBUser:
    query = select(models.DBUser)
    users = await db.execute(query)
    return users.scalar()


async def get_user_by_id(db: AsyncSession, user_id: int) -> models.DBUser | None:
    query = select(models.DBUser).where(models.DBUser.id == user_id)
    user = await db.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> models.DBUser | None:
    query = select(models.DBUser).where(models.DBUser.email == email)
    user = await db.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.DBUser:
    user.password = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    query = insert(models.DBUser).values(**user.model_dump())
    new_user = await db.execute(query)
    new_user = new_user.scalar_one()
    await db.commit()
    return new_user


async def update_user_thread_id_by_email(
    db: AsyncSession, email: str, thread_id: str
) -> models.DBUser:
    query = (
        update(models.DBUser)
        .where(models.DBUser.email == email)
        .values(thread_id=thread_id)
    )
    updated_user = await db.execute(query)
    await db.commit()
    return updated_user


async def authenticate_user(
    db: AsyncSession, user: schemas.UserCreate
) -> models.DBUser:
    user_db = await get_user_by_email(db, user.email)
    form_password = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    if user_db and user_db.password != form_password:
        raise HTTPException(status_code=401, detail="Credentials are incorrect")
    return user_db
