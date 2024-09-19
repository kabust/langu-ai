from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from gpt.gpt_client_handler import GPTClientHandler
from gpt.config import client


router = APIRouter()
gpt_client_handler = GPTClientHandler(client=client)


@router.post("/completion/")
async def completion(prompt: str, db: AsyncSession = Depends(get_db)):
    client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content":
                    """
                    You are a language tutor, use simple language as a real teacher and
                    try to lead the conversation. Imagine that you have a 1 on 1 in-person meeting. 
                    Also, emphasise grammatical and logical mistakes, but keep the dialog casual and engaging.
                    """
                 },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
    )


@router.post("/transcription/")
async def transcription(file: UploadFile, db: AsyncSession = Depends(get_db)):
    audio_bytes = await file.read()
    response = gpt_client_handler.speech_to_text(audio_bytes)
    return {"transcription": response}
