import os
from dotenv import load_dotenv
from groq import Groq



load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq()
async def model_groq(prompt: str):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content":"You are Torch Labs' official assistant. Answer in a professional tone, as a company representative."
                "If the answer is not found in the context, respond with: We’re sorry, but we currently do not have updated information on that topic. Please feel free to reach out to our support team for further assistance."
                "Remember do not mention anything about missing context, AI limitations, or system behavior. Always speak as a representative of Torch Labs using phrases like 'we', 'our company', 'Torch Labs offers', etc."
                "Remeber avoid phrases like 'Based on the context', 'The context provided' and 'Context' likewise"
              
                
            },
            
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

