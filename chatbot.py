import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)


def generate_answer(messages, system_prompt=None):

    if system_prompt is None:
        system_prompt = SYSTEM_PROMPT

    history = [
        SystemMessage(content=system_prompt)
    ]

    for msg in messages:

        if msg["role"] == "user":

            history.append(
                HumanMessage(content=msg["content"])
            )

        else:

            history.append(
                AIMessage(content=msg["content"])
            )

    response = llm.invoke(history)

    return response.content