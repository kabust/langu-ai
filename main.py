import os
import time
import numpy as np

from config import client
from audio_input import AudioHandler


def main() -> None:
    audio_handler = AudioHandler(client=client)
    prompt_from_speech = audio_handler.speech_to_text()

    start = time.time()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a language tutor."},
            {
                "role": "user",
                "content": prompt_from_speech
            }
        ]
    )
    print("Took:", time.time() - start)
    print(completion.choices[0].message.content)


if __name__ == '__main__':
    main()
