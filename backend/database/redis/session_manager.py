import json

from .redis_client import redis_client


class SessionManager:

    def create_session(
        self,
        session_id,
        payload,
        ttl=3600
    ):

        redis_client.setex(
            session_id,
            ttl,
            json.dumps(payload)
        )

    def get_session(
        self,
        session_id
    ):

        data = redis_client.get(
            session_id
        )

        if not data:

            return None

        return json.loads(data)

    def delete_session(
        self,
        session_id
    ):

        redis_client.delete(
            session_id
        )