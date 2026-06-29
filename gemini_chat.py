import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from chatbot import generate_answer

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
    try :

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
    except Exception as e:

     error = str(e)

    if (
        "429" in error
        or "RESOURCE_EXHAUSTED" in error
    ):

        fallback_messages = []

        for msg in messages:

            fallback_messages.append(
                {
                    "role": msg["role"],
                    "content": msg["content"],
                }
            )

        answer = generate_answer(fallback_messages)

        return (
            "⚠️ Gemini is temporarily busy.\n\n"
            "🔄 Switched to Groq.\n\n"
            + answer
        )

    return f"Gemini Error:\n{error}"