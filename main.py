from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from settings import settings
from gpt.routes import router as gpt_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(gpt_router, prefix="/gpt")

templates = settings.TEMPLATES


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
