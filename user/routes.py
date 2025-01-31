from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from user import crud, schemas, models
from dependencies import get_db


router = APIRouter()
templates = settings.TEMPLATES


@router.get("/", response_model=List[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_users(db)


@router.get("/<int:user_id>", response_model=schemas.User)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_id(db, user_id)


@router.get("/<int:user_email>", response_model=schemas.User)
async def read_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_email(db, email)


@router.get("/register", response_model=schemas.UserCreate)
async def register_user(request: Request, db: AsyncSession = Depends(get_db)):
    if request.method == "POST":
        user = models.DBUser(**request.data)
        return await crud.create_user(db)
    
    if request.method == "GET":
        context = {"schema": schemas.UserCreate.model_json_schema()}
        return templates.TemplateResponse(
            request=request, name="register.html", context=context
        )
    