from app.cache_service import create_cache_key,get_cached_response, set_cached_response, add_to_user_history, get_user_history
from app.groq_service import generate_llm_response
from fastapi import FastAPI, Query
from app.retriever import retrieve_chunks

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Assistant API!"}

@app.get("/retrieve-context")
def retrieve_context(
    customer_type: str = Query(..., enum=["enterprise", "admin"]),
    query: str = Query(...)
):
    return retrieve_chunks(customer_type, query)

@app.get("/generate-response")
async def generate_response(customer_type: str = Query(..., enum=["enterprise", "admin"]), question: str = Query(...), user_id: str = Query(...)):
    # Cache key
    cache_key = create_cache_key(customer_type, question)
    cached = get_cached_response(cache_key)

    if cached:
        return {"cached": True, "response": cached.decode()}

    # Retrieve relevant chunks for context
    context = retrieve_chunks(customer_type, question)
    
    # Get user's previous Q&A for session context
    user_history = get_user_history(user_id)
    history_str = "\n".join([f"Previous Question: {item['question']}\n" for item in user_history])

    prompt = f"""
    You are a helpful representative of Torch Labs. Use the following context and the customer’s previous questions to answer professionally. If the answer is not found in the context, respond with:

    "We’re sorry, but we currently do not have updated information on that topic. Please feel free to reach out to our support team for further assistance."

    Do not mention missing context, AI limitations, or system behavior. Speak as a Torch Labs rep using "we", "our company", etc.

    Customer History:(This will help you understand the customer's previous questions and context)
    {history_str}

    Current Question: {question}:(This is the current question from the customer)

    Context:(This is the context retrieved from the database)
    {context['results']} 
    """

    # Call LLM
    ai_response = await generate_llm_response(prompt)

    # Save to cache
    set_cached_response(cache_key, ai_response)

    # Save to user session
    add_to_user_history(user_id, question, ai_response)

    return {"cached": False, "response": ai_response}