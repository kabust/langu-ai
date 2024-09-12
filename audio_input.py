import sounddevice as sd
import numpy as np
from openai import OpenAI

# import scipy.io.wavfile as wav


class AudioHandler:
    def __init__(self, client: OpenAI) -> None:
        self.client = client
        self.fs = 44100
        self.duration = 5  # seconds

    def stream_audio_input(self) -> np.ndarray:
        print("Talk...")
        my_recording = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=2, dtype='float64')
        sd.wait()
        return my_recording

    def speech_to_text(self, audio: np.ndarray | None = None) -> str:
        if not audio:
            audio = self.stream_audio_input()

        audio.tofile("audio.mp3")
        audio = open("audio.mp3", "rb")

        transcription = self.client.audio.transcriptions.create(
            file=audio,
            model="whisper-1",
            response_format="text",
        )
        return transcription.text

# print("Playing the recording")
# sd.play(my_recording, fs)
# sd.wait()
