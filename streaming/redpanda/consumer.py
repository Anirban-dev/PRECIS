from kafka import KafkaConsumer
import json


class RedpandaConsumer:

    def consume(
        self,
        topic
    ):

        consumer = KafkaConsumer(
            topic,
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda value: json.loads(
                value.decode()
            )
        )

        for message in consumer:

            yield message.value