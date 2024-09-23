import io
import os
from pathlib import Path
from typing import BinaryIO

import speech_recognition as sr

from openai import OpenAI


class GPTClientHandler:
    def __init__(self, client: OpenAI, assistant_id: str) -> None:
        self.client = client
        self.assistant_id = assistant_id
        self.recognizer = sr.Recognizer()

    def completion(self, prompt: str, thread_id: str):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=prompt
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id
            )
            response = messages.data[0].content[0].text.value
            print(response)
            return {"response": response}
        else:
            print(run.status)

    def speech_to_text(self, audio_bytes: bytes) -> str:
        try:
            filename = "recording.mp3"
            buffer = io.BytesIO(audio_bytes)
            buffer.name = filename

            transcript = self.client.audio.transcriptions.create(model="whisper-1", file=buffer)

            text = transcript.text
            return text

        except Exception as e:
            print(e)

    def text_to_speech(self, speech: str) -> bytes:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=speech,
            response_format="mp3"
        )
        return response.content
