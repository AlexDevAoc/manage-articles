import json
import os
import redis
from .articles.models import Article as ArticleSchema

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(REDIS_URL)

# TTL por defecto en segundos
DEFAULT_TTL = int(os.getenv("ARTICLE_CACHE_TTL"))

def get_article_cache(article_id: int):
	key = f"article:{article_id}"
	cached = redis_client.get(key)
	if cached:
		return json.loads(cached)
	return None

def set_article_cache(article_id: int, data: ArticleSchema, ttl: int = DEFAULT_TTL):
	key = f"article:{article_id}"
	redis_client.setex(key, ttl, data.model_dump_json())

def invalidate_article_cache(article_id: int):
	key = f"article:{article_id}"
	redis_client.delete(key)