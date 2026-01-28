import redis
import os

REDIS_URL = os.getenv("REDIS_URL")

# Initialize redis cache client
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
