from .redis_client import redis_client


class PubSubManager:

    def publish(
        self,
        channel,
        payload
    ):

        redis_client.publish(
            channel,
            payload
        )

    def subscribe(
        self,
        channel
    ):

        subscriber = redis_client.pubsub()

        subscriber.subscribe(
            channel
        )

        return subscriber