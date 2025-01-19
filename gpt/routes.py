from fastapi import APIRouter, Depends, HTTPException, UploadFile, requests, WebSocket
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from dependencies import get_db
from gpt.gpt_client_handler import GPTClientHandler
from gpt.config import client, assistant_id, TOKEN


router = APIRouter()
gpt_client_handler = GPTClientHandler(client=client, token=TOKEN)
templates = settings.TEMPLATES


@router.post("/completion/")
async def completion(prompt: str, db: AsyncSession = Depends(get_db)):
    if not requests.Request.user:
        thread = client.beta.threads.create()
    else:
        ...

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant_id, instructions=prompt
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        print(response)
        return {"response": response}
    else:
        print(run.status)


@router.post("/transcription/")
async def transcription(file: UploadFile, db: AsyncSession = Depends(get_db)):
    audio_bytes = await file.read()
    response = gpt_client_handler.speech_to_text(audio_bytes)
    return {"transcription": response}
