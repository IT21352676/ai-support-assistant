from app.cache_service import create_cache_key, get_cached_response, set_cached_response
from app.groq_service import generate_llm_response
from fastapi import FastAPI, Query
from app.retriever import retrieve_chunks

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Assistant API!"}

@app.get("/retrieve-context")
def retrieve_context(
    customer_type: str = Query(..., enum=["enterprise", "individual"]),
    query: str = Query(...)
):
    return retrieve_chunks(customer_type, query)

@app.get("/generate-response")
async def generate_response(customer_type: str = Query(...), question: str = Query(...)):
    # Cache key
    cache_key = create_cache_key(customer_type, question)
    cached = get_cached_response(cache_key)

    if cached:
        return {"cached": True, "response": cached.decode()}

    # Retrieve relevant chunks
    context = retrieve_chunks(customer_type, question)

    prompt = f"""Answer the following based on the context below:
Context: {context['results']}
Question: {question}"""

    # Call LLM
    ai_response = await generate_llm_response(prompt)

    # Save to cache
    set_cached_response(cache_key, ai_response)

    return {"cached": False, "response": ai_response}