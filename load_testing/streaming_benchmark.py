from streaming.event_bus.publisher import EventPublisher


publisher = EventPublisher()

for index in range(1000):

    publisher.publish(

        "benchmark",

        {

            "index":
                index
        }
    )