import io
import os
from pathlib import Path
from typing import BinaryIO

import sounddevice as sd
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import numpy as np

from openai import OpenAI


class GPTClientHandler:
    def __init__(self, client: OpenAI) -> None:
        self.client = client
        self.recognizer = sr.Recognizer()
        self.record_audio_path = Path(__file__).parent / "recording.mp3"
        self.response_audio_path = Path(__file__).parent / "response.mp3"

    def record_audio(self) -> BinaryIO:
        try:
            print("Talk...")
            with sr.Microphone() as source2:
                self.recognizer.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = self.recognizer.listen(source2)

                print("Getting text...")
                with open(self.record_audio_path, "wb") as f:
                    f.write(audio2.get_wav_data())
                    return f

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")

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

    def text_to_speech(self, speech: str) -> None:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=speech
        )
        response.stream_to_file(self.response_audio_path)

    def play_audio(self) -> None:
        print("Playing response")
        if os.name != "nt":
            try:
                os.system(f"start cmd /C \"afplay {self.response_audio_path}\"")
            # except Exception:
            #     os.system(f"start cmd /C \"mpg123 {response_file_path}\"")
            except FileNotFoundError:
                print("File not found, can't play audio")
        else:
            audio_response = AudioSegment.from_mp3(self.response_audio_path)
            play(audio_response)
