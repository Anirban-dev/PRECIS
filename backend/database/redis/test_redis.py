from backend.database.redis.redis_client import (
    RedisClient
)

redis = RedisClient.get_client()

redis.set(
    "precis_test",
    "working"
)

print(
    redis.get(
        "precis_test"
    )
)