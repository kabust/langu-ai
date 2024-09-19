import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("OPENAI_TOKEN")

client = OpenAI(api_key=TOKEN)

assistant = client.beta.assistants.create(
    name="Language Tutor",
    instructions="""
    You are a language tutor, use simple language as a real teacher and
    try to lead the conversation. Imagine that you have a 1 on 1 in-person meeting. 
    Also, emphasise grammatical and logical mistakes, but keep the dialog casual and engaging.
    """,
    model="gpt-4o-mini",
)
