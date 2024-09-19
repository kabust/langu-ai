from fastapi import FastAPI

from gpt.routes import router as gpt_router

app = FastAPI()

app.include_router(gpt_router, prefix="/gpt")
# app.include_router(temperature_router)


@app.get("/")
def index():
    return {
        "Docs": "/docs/",
        "Request speech transcription": app.url_path_for("transcription")
    }
