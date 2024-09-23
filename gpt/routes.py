from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from gpt.gpt_client_handler import GPTClientHandler
from gpt.config import client, assistant_id

router = APIRouter()
gpt_client_handler = GPTClientHandler(client=client, assistant_id=assistant_id)


@router.post("/completion/")
async def completion(prompt: str, db: AsyncSession = Depends(get_db)) -> dict:
    thread = client.beta.threads.create()
    return gpt_client_handler.completion(prompt, thread.id)


@router.post("/transcription/")
async def transcription(file: UploadFile, db: AsyncSession = Depends(get_db)) -> dict:
    audio_bytes = await file.read()
    response = gpt_client_handler.speech_to_text(audio_bytes)
    return {"transcription": response}


@router.get("/tts/")
async def text_to_speech(text: str, db: AsyncSession = Depends(get_db)) -> Response:
    audio = gpt_client_handler.text_to_speech(text)
    return Response(content=audio, media_type="audio/mp3")
