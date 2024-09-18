import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("OPENAI_TOKEN")

client = OpenAI(api_key=TOKEN)
