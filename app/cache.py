import json
import os
import redis

_client: redis.Redis | None = None

def get_cache() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'), decode_responses=True)
    return _client

def cache_get(key: str):
    data = get_cache().get(key)
    if data is None:
        return None
    try:
        return json.loads(str(data))
    except json.JSONDecodeError:
        return None

def cache_set(key: str, value, ttl: int = 60):
    get_cache().setex(key, ttl, json.dumps(value))

def cache_delete(*keys: str):
    get_cache().delete(*keys)
