import json
import logging
import os
import redis

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None

def get_cache() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'), decode_responses=True)
    return _client

def cache_get(key: str):
    try:
        data = get_cache().get(key)
        if data is None:
            return None
        return json.loads(str(data))
    except (redis.RedisError, json.JSONDecodeError) as e:
        logger.warning("cache_get failed: %s", e)
        return None

def cache_set(key: str, value, ttl: int = 60):
    try:
        get_cache().setex(key, ttl, json.dumps(value))
    except redis.RedisError as e:
        logger.warning("cache_set failed: %s", e)

def cache_delete(*keys: str):
    try:
        get_cache().delete(*keys)
    except redis.RedisError as e:
        logger.warning("cache_delete failed: %s", e)
