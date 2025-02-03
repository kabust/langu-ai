from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from dependencies import get_current_user_email, get_db
from settings import settings
from gpt.routes import router as gpt_router
from user.crud import get_user_by_email
from user.routes import router as user_router
from user.schemas import UserCreate


app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

app.include_router(gpt_router, prefix="/gpt")
app.include_router(user_router, prefix="/user")


templates = settings.TEMPLATES


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request, 
    db: AsyncSession = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    try:
        user = await get_user_by_email(db, user_email)
    except HTTPException:
        user = None
    context = {"user": user}
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.post("/set_languages")
async def set_languages(
    languageNative: str = Form(examples=["Ukrainian", "Polish", "English"]),
    languageToLearn: str = Form(examples=["Ukrainian", "Polish", "English"])
):
    response = Response()
    response.set_cookie(key="languageNative", value=languageNative, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MS)
    response.set_cookie(key="languageToLearn", value=languageToLearn, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MS)
    return response


@app.get("/get_languages")
async def get_languages(request: Request):
    languageNative = request.cookies.get("languageNative")
    languageToLearn = request.cookies.get("languageToLearn")
    return {"languageNative": languageNative, "languageToLearn": languageToLearn}


@app.exception_handler(401)
async def unauthorized_redirect(*args, **kwargs):
    return RedirectResponse("/user/login")
