import urllib
import yaml

from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
)
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user_email, get_db
from settings import settings
from gpt.gpt_client_handler import GPTClientHandler
from gpt.config import client, ASSISTANT_ID, TOKEN
from user.crud import get_user_by_email, update_user_thread_id_by_email


router = APIRouter()
gpt_client_handler = GPTClientHandler(
    client=client, assistant_id=ASSISTANT_ID, token=TOKEN
)
templates = settings.TEMPLATES


@router.get("/init_lesson")
async def init_lesson(
    request: Request,
    user_email: str = Depends(get_current_user_email),
    db: AsyncSession = Depends(get_db),
) -> Response:
    languageNative = request.cookies.get("languageNative")
    languageToLearn = request.cookies.get("languageToLearn")
    user = await get_user_by_email(db, user_email)

    with open("gpt/languages.yaml", "r", encoding="utf8") as file:
        languages_map = yaml.safe_load(file)

    if not user.thread_id:
        thread = client.beta.threads.create()
        user = await update_user_thread_id_by_email(db, user_email, thread.id)

        message = languages_map["languages"]["no_thread_init"][languageNative].format(
            language=languages_map[languageNative][languageToLearn]
        )
        client.beta.threads.messages.create(
            thread_id=thread.id, content=message, role="assistant"
        )
    else:
        thread = client.beta.threads.retrieve(user.thread_id)
        thread_messages = client.beta.threads.messages.list(thread.id)

        try:
            last_message = thread_messages.data[0].content[0].text.value

            topic = gpt_client_handler.completion(
                f"Create a short summary (up to 10 words) for this topic: {last_message}",
                thread.id
            )

            message = languages_map["languages"]["thread_init"][
                "has_message"
            ][languageNative].format(last_message=topic)
        except (IndexError, KeyError) as e:
            message = languages_map["languages"]["thread_init"]["no_message"][languageNative]
    audio = gpt_client_handler.text_to_speech(message)

    response = Response(content=audio, media_type="audio/mpeg")
    encoded_message = urllib.parse.quote(message)
    response.headers["X-Message"] = encoded_message
    return response


@router.post("/prepare_answer")
async def prepare_answer(
    file: UploadFile,
    user_email: str = Depends(get_current_user_email),
    db: AsyncSession = Depends(get_db),
) -> Response:
    user = await get_user_by_email(db, user_email)
    audio_bytes = await file.read()
    transcription = gpt_client_handler.speech_to_text(audio_bytes)

    if not transcription:
        raise HTTPException(500, "Couldn't get the transcription")

    gpt_response = gpt_client_handler.completion(transcription, user.thread_id)

    audio = gpt_client_handler.text_to_speech(gpt_response)
    print(transcription)
    print(gpt_response)

    response = Response(content=audio, media_type="audio/mpeg")
    encoded_message = urllib.parse.quote(gpt_response)
    response.headers["X-Message"] = encoded_message
    return response


@router.post("/completion")
async def completion(prompt: str, thread_id: str):
    response = gpt_client_handler.completion(prompt, thread_id)
    return response


@router.post("/transcription")
async def transcription(file: UploadFile) -> dict:
    audio_bytes = await file.read()
    response = gpt_client_handler.speech_to_text(audio_bytes)
    return {"transcription": response}


@router.get("/tts")
async def text_to_speech(text: str) -> Response:
    audio = gpt_client_handler.text_to_speech(text)
    return Response(content=audio, media_type="audio/mpeg")
