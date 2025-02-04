import yaml

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    UploadFile,
    WebSocket
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user_email, get_db
from settings import settings
from gpt.gpt_client_handler import GPTClientHandler
from gpt.config import client, assistant_id, ASSISTANT_ID, TOKEN
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

    if not user.thread_id:
        print("User has thread_id")
        with open("gpt/languages.yaml", "r", encoding="utf8") as file:
            languages_map = yaml.safe_load(file)

        thread = client.beta.threads.create()
        user = await update_user_thread_id_by_email(db, user_email, thread.id)

        message = languages_map["languages"][languageNative].format(
            language=languages_map[languageNative][languageToLearn]
        )
        print(message)
        client.beta.threads.messages.create(
            thread_id=thread.id, content=message, role="assistant"
        )
    else:
        print("User doesn't have thread_id")
        thread = client.beta.threads.retrieve(user.thread_id)
        thread_messages = client.beta.threads.messages.list(thread.id)
        thread_messages = thread_messages.model_dump()
        last_id = thread_messages["last_id"]
        try:
            last_message = [
                message["content"]["value"] 
                for message in thread_messages["data"]
                if message.get("last_id") == last_id
            ][0]
            message = f"Let's begin our lesson, we stopped on {last_message}, do you have anything specific on mind to discuss now?"
        except (IndexError, KeyError) as e:
            message = f"Hmmm... Could you remind me where we finished previously? Seems like I forgot our last topic."

    audio = gpt_client_handler.text_to_speech(message)
    return Response(content=audio, media_type="audio/mpeg", headers={"X-Message": message})


@router.post("/process_recording")
async def process_recording(
    file: UploadFile,
    user_email: str = Depends(get_current_user_email),
    db: AsyncSession = Depends(get_db),
) -> Response:
    try:
        user = await get_user_by_email(db, user_email)

        audio_bytes = await file.read()
        transcription = gpt_client_handler.speech_to_text(audio_bytes)
        print(transcription)
        gpt_response = gpt_client_handler.completion(transcription, user.thread_id)
        print(gpt_response)
        return Response(gpt_response)
    except Exception as e:
        return Response(f"Couldn't process the recording: {e}", 500)


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
