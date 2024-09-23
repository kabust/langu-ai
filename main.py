from fastapi import FastAPI

from gpt.routes import router as gpt_router
from user.routes import router as user_router

app = FastAPI()

app.include_router(gpt_router, prefix="/gpt")
app.include_router(user_router, prefix="/user")


@app.get("/")
def index():
    return {
        "Docs": "/docs/",
        "Request speech transcription": app.url_path_for("transcription")
    }
