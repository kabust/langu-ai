import os
import time

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
TOKEN = os.getenv("OPENAI_TOKEN")


def main() -> None:
    client = OpenAI(api_key=TOKEN)
    start = time.time()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    )
    print("Took:", time.time() - start)
    print(completion.choices[0].message)


if __name__ == '__main__':
    main()
