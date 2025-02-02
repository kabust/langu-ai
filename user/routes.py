from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Form

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from user import crud, schemas, models
from dependencies import get_db
from user.jwt import create_access_token


router = APIRouter()
templates = settings.TEMPLATES


@router.get("/", response_model=List[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_users(db)


@router.get("/<int:user_id>", response_model=schemas.User)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_id(db, user_id)


@router.get("/<str:user_email>", response_model=schemas.User)
async def read_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_email(db, email)


@router.get("/register", response_model=schemas.UserCreate)
async def register_user(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse(
        request=request, name="register.html"
    )


@router.post("/register", response_model=schemas.UserCreate)
async def register_user(
    request: Request, 
    email: str = Form(pattern=r"[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]+"),
    password: str = Form(min_length=6),
    db: AsyncSession = Depends(get_db)
):
    try:
        print(email, password)
        user = schemas.UserCreate(email=email, password=password)
        await crud.create_user(db, user)
        return templates.TemplateResponse(
            request=request, name="login.html"
        )
    except IntegrityError:
        error = "User with this email already exists"
    except Exception:
        error = "Error during register"

    context = {"error": error}
    return templates.TemplateResponse(
        request=request, name="register.html", context=context
    )


@router.get("/login", response_model=schemas.User)
async def login_user(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )


@router.post("/login")
async def login_user(    
    request: Request, 
    email: str = Form(pattern=r"[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]+"),
    password: str = Form(min_length=6),
    db: AsyncSession = Depends(get_db)
):
    try:
        user = schemas.UserCreate(email=email, password=password)
        await crud.authenticate_user(db, user)
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
