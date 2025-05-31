import redis
import hashlib
import os

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def create_cache_key(customer_type: str, question: str) -> str:
    key = f"{customer_type}:{question}"
    return hashlib.sha256(key.encode()).hexdigest()

def get_cached_response(key: str):
    return redis_client.get(key)

def set_cached_response(key: str, value: str):
    redis_client.set(key, value)
