import redis
import hashlib
import os
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def create_cache_key(customer_type: str, question: str) -> str:
    key = f"{customer_type}:{question}"
    return hashlib.sha256(key.encode()).hexdigest()

def get_cached_response(key: str):
    return redis_client.get(key)

def set_cached_response(key: str, value: str):
    redis_client.set(key, value)

def add_to_user_history(user_id: str, question: str, answer: str):
    history_key = f"user_history:{user_id}"
    entry = json.dumps({"question": question, "answer": answer})
    redis_client.rpush(history_key, entry)
    # redis_client.ltrim(history_key, -1,-5)  # Keep only last 5 entries

def get_user_history(user_id: str):
    history_key = f"user_history:{user_id}"
    history_data = redis_client.lrange(history_key, 0, -1)
    return [json.loads(h.decode()) for h in history_data]