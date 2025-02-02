from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from dependencies import get_current_user, get_db
from settings import settings
from gpt.routes import router as gpt_router
from user.crud import get_user_by_email
from user.routes import router as user_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

app.include_router(gpt_router, prefix="/gpt")
app.include_router(user_router, prefix="/user")


templates = settings.TEMPLATES


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user: dict = None):
    try:
        return templates.TemplateResponse(
            request=request, name="index.html"
        )
    except HTTPException:
        return RedirectResponse("/user/login")
    

@app.post("/", response_class=HTMLResponse)
async def index(user: dict = None):
    try:
        context = {}
        if user:
            context.update(user=user)
        return templates.TemplateResponse(
            name="index.html", context=context
        )
    except HTTPException:
        return RedirectResponse("/user/login")


@app.get("/auth")
async def auth_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    user = await get_user_by_email(db, current_user)
    request.state.user = user
    return user
