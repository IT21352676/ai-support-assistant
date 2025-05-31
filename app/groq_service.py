import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = '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'
# os.getenv("OPENROUTER_API_KEY")

async def generate_llm_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
