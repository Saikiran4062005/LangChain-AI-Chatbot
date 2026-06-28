import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_gemini(messages):

    # Keep only recent conversation
    messages = messages[-10:]

    history = ""

    for msg in messages:
        role = msg["role"].capitalize()
        history += f"{role}: {msg['content']}\n"

    last_prompt = messages[-1]["content"].lower()

    web_keywords = [
        "latest",
        "today",
        "current",
        "news",
        "weather",
        "live",
        "2026",
        "score",
        "stock",
        "price",
        "breaking",
    ]

    use_web = any(
        word in last_prompt
        for word in web_keywords
    )

    if use_web:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ],
                response_modalities=["TEXT"],
            ),
        )

    else:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
        )

    return response.text