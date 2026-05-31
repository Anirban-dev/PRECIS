import json

from backend.database.redis.redis_client import (
    RedisClient
)


class SessionManager:

    def __init__(self):

        self.redis = (
            RedisClient.get_client()
        )

    def create_session(

        self,

        user_id,

        data
    ):

        self.redis.set(

            f"session:{user_id}",

            json.dumps(data)
        )

    def get_session(

        self,

        user_id
    ):

        return self.redis.get(

            f"session:{user_id}"
        )