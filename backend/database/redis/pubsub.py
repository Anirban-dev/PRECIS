from backend.database.redis.redis_client import (
    RedisClient
)


class PubSubManager:

    def __init__(self):

        self.redis = (
            RedisClient.get_client()
        )

    def publish(

        self,

        channel,

        payload
    ):

        self.redis.publish(

            channel,

            payload
        )