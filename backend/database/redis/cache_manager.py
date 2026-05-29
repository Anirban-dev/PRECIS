from .redis_client import redis_client


class CacheManager:

    def set_cache(
        self,
        key,
        value,
        expiry=300
    ):

        redis_client.setex(
            key,
            expiry,
            value
        )

    def get_cache(
        self,
        key
    ):

        return redis_client.get(key)

    def delete_cache(
        self,
        key
    ):

        redis_client.delete(key)

    def exists(
        self,
        key
    ):

        return redis_client.exists(key)