import os
import time
import numpy as np

from config import client
from gpt_client_handler import GPTClientHandler


def main() -> None:
    audio_handler = GPTClientHandler(client=client)

    while True:
        prompt_from_speech = audio_handler.speech_to_text()

        start = time.time()
        completion = client.chat.completions.create(
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
                    "content": prompt_from_speech
                }
            ]
        )
        response = completion.choices[0].message.content
        print("Took:", time.time() - start)
        print(response)
        audio_handler.text_to_speech(response)


if __name__ == '__main__':
    main()
