import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "nats-subscriber"
)


class NATSSubscriber:

    def __init__(self):

        logger.info(
            "Initializing NATS Subscriber..."
        )

    async def listen(

        self,

        subject="precis.alerts"
    ):

        logger.info(

            f"Listening to subject: "

            f"{subject}"
        )

        while True:

            await asyncio.sleep(5)

            logger.info(

                f"[NATS EVENT] "

                f"Received event from {subject}"
            )


if __name__ == "__main__":

    subscriber = NATSSubscriber()

    asyncio.run(
        subscriber.listen()
    )