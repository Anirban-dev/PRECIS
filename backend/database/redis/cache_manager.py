from backend.database.redis.redis_client import (
    RedisClient
)


class CacheManager:

    def __init__(self):

        self.redis = (
            RedisClient.get_client()
        )

    def set(

        self,

        key,

        value,

        ttl=300
    ):

        self.redis.setex(

            key,

            ttl,

            value
        )

    def get(

        self,

        key
    ):

        return self.redis.get(
            key
        )