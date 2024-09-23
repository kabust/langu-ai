from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from user import crud, schemas
from dependencies import get_db


router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_users(db)


@router.get("/<int:user_id>", response_model=schemas.User)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_id(db, user_id)


@router.get("/<int:user_email>", response_model=schemas.User)
async def read_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_email(db, email)
