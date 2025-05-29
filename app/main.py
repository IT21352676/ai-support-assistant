from fastapi import FastAPI, Query
from app.retriever import retrieve_chunks

app = FastAPI()

@app.get("/retrieve-context")
def retrieve_context(
    customer_type: str = Query(..., enum=["enterprise", "individual"]),
    query: str = Query(...)
):
    return retrieve_chunks(customer_type, query)
