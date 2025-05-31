import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


async def generate_llm_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data=json.dumps({
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [
      {
        "role": "user",
        "content": prompt
      }
    ],
    
  })

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", data=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
