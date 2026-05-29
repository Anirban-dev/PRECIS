from kafka import KafkaProducer
import json


class RedpandaProducer:

    def __init__(self):

        self.producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda value: json.dumps(
                value
            ).encode()
        )

    def publish(
        self,
        topic,
        payload
    ):

        self.producer.send(
            topic,
            payload
        )

        self.producer.flush()

        return {
            "topic": topic,
            "status": "PUBLISHED"
        }