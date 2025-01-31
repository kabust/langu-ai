import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("OPENAI_TOKEN")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=TOKEN)
assistant_id = ASSISTANT_ID
