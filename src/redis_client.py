import os
import redis.asyncio as redis
from dotenv import load_dotenv


load_dotenv()


redis_client = redis.Redis(
    host='bursting-marlin-38619.upstash.io',
    port=6379,
    password=os.environ.get("UPSTASH_REDIS_API_KEY"),
    ssl=True,
)
