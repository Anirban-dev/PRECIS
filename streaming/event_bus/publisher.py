class EventPublisher:

    def publish(
        self,
        topic,
        payload
    ):

        return {

            "topic":
                topic,

            "payload":
                payload,

            "status":
                "PUBLISHED"
        }