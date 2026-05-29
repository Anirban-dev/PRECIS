import redis


class RedisClient:

    def __init__(self):

        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    def get_client(self):

        return self.client


redis_client = RedisClient().get_client()