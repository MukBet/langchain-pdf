import os, redis

redis_client = redis.from_url(
    os.getenv("REDIS_URI"),
    decode_responses=True
)