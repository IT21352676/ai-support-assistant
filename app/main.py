from app.cache_service import create_cache_key,get_cached_response, set_cached_response, add_to_user_history, get_user_history
from app.groq_service import model_groq
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
async def generate_response(customer_name:str=Query(...), customer_type: str = Query(..., enum=["enterprise", "admin"]), question: str = Query(...), user_id: str = Query(...)):
    # Cache key
    cache_key = create_cache_key(user_id,customer_type, question)
    cached = get_cached_response(cache_key)

    if cached:
        return {"cached": True, "response": cached.decode()}

    # Retrieve relevant chunks for context
    context = retrieve_chunks(customer_type, question)
    
    # Get user's previous Q&A for session context
    user_history = get_user_history(user_id)
    
    history_str = "\n".join([f"Previous Question: {item['question']}\n" for item in user_history])
    
    prompt = f"""
    Customer Name : {customer_name}

    Customer History:(This will help you understand the customer's previous questions and context)
    {history_str}

    Customer Current Question: {question}:(This is the current question from the customer)

    Context:(This is the context retrieved from the database, sometimes it might be unrelevant(Like situation greetings , thankings etc) to the question, so you need to understand the context and then answer the question){context['results']} 
    """

    # Call LLM
    ai_response = await model_groq(prompt)


    # Save to cache
    set_cached_response(cache_key, ai_response)

    # Save to user session
    add_to_user_history(user_id, question, ai_response)

    return {"cached": False, "response": ai_response}

@app.get("/get-user-history")
async def get_history(user_id: str = Query(...)):
    user_history =get_user_history(user_id)
    history_str = "\n".join([f"{item['question']}\n" for item in user_history])
    return {"history":history_str}

    
