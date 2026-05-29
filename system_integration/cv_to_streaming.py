from streaming.event_bus.publisher import EventPublisher


class CVToStreaming:

    def __init__(self):

        self.publisher = EventPublisher()

    def publish_optical_flow(

        self,

        payload
    ):

        return self.publisher.publish(

            "cv-optical-flow",

            payload
        )

    def publish_turbulence(

        self,

        payload
    ):

        return self.publisher.publish(

            "cv-turbulence",

            payload
        )