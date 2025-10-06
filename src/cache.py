import json
import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)

# TTL por defecto en segundos
DEFAULT_TTL = int(os.getenv("ARTICLE_CACHE_TTL", "120"))

def get_article_cache(article_id: int):
	key = f"article:{article_id}"
	cached = redis_client.get(key)
	if cached:
		return json.loads(cached)
	return None

def set_article_cache(article_id: int, data: dict, ttl: int = DEFAULT_TTL):
	key = f"article:{article_id}"
	redis_client.setex(key, ttl, json.dumps(data.dict()))

def invalidate_article_cache(article_id: int):
	key = f"article:{article_id}"
	redis_client.delete(key)