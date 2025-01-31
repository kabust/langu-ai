from fastapi import APIRouter, Depends, HTTPException, UploadFile, requests, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from gpt.gpt_client_handler import GPTClientHandler
from gpt.config import client, assistant_id, ASSISTANT_ID, TOKEN


router = APIRouter()
gpt_client_handler = GPTClientHandler(client=client, assistant_id=ASSISTANT_ID, token=TOKEN)
templates = settings.TEMPLATES


@router.post("/completion/")
async def completion(prompt: str, thread_id: str = None):
    if not thread_id:
        thread = client.beta.threads.create()
        response = text_to_speech("")
        return {"thread_id": thread.id}
    else:
        thread = client.beta.threads.retrieve(thread_id)

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
async def transcription(file: UploadFile) -> dict:
    audio_bytes = await file.read()
    response = gpt_client_handler.speech_to_text(audio_bytes)
    return {"transcription": response}


@router.get("/tts/")
async def text_to_speech(text: str) -> Response:
    audio = gpt_client_handler.text_to_speech(text)
    return Response(content=audio, media_type="audio/mp3")
