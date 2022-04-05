import os
import redis

r = redis.Redis(
    decode_responses=True,
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    db=0)
