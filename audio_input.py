from pathlib import Path

import sounddevice as sd
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import numpy as np

from openai import OpenAI


class AudioHandler:
    def __init__(self, client: OpenAI) -> None:
        self.client = client
        self.fs = 44100
        self.duration = 5  # seconds
        self.recognizer = sr.Recognizer()

    def stream_audio_input(self) -> np.ndarray:
        print("Talk...")
        my_recording = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=2, dtype='float64')
        sd.wait()
        return my_recording

    def speech_to_text(self, audio: np.ndarray | None = None) -> str:
        try:
            print("Talk...")
            with sr.Microphone() as source2:
                self.recognizer.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = self.recognizer.listen(source2)

                print("Getting text...")
                audio_file_path = Path(__file__).parent / "speech.wav"
                with open(audio_file_path, "wb") as f:
                    f.write(audio2.get_wav_data())

                with open(audio_file_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(model="whisper-1", file=audio_file)

                text = transcript.text
                print(text)
                return text

        except sr.RequestError as e:
            print(e)

        except sr.UnknownValueError as e:
            print(e)

    def text_to_speech(self, speech: str) -> None:
        response_file_path = Path(__file__).parent / "response.mp3"

        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=speech
        )
        response.stream_to_file(response_file_path)

        audio_response = AudioSegment.from_mp3(response_file_path)
        print("Playing response")
        print(response_file_path)
        play(audio_response)
