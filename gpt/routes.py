from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter()


# @router.get("/cities/", response_model=list[schemas.City])
# async def read_all_cities(db: AsyncSession = Depends(get_db)):
#     return await crud.get_all_cities(db)
