import os
import asyncio
from dotenv import load_dotenv

from groq import Groq

load_dotenv()


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


async def send_article_then_summarize(article: str) -> str:
    chat_completion = await asyncio.to_thread(
        client.chat.completions.create,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this article: '{article}'",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content
