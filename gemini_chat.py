import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_gemini(messages):
    messages = messages[-10:]

    history = ""

    for msg in messages:
        role = msg["role"].capitalize()
        history += f"{role}: {msg['content']}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history,
        
    )

    return response.text