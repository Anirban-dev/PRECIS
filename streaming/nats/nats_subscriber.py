import json

from streaming.nats.nats_client import NATSClient


class NATSSubscriber:

    def __init__(self):

        self.client = NATSClient()

    async def subscribe(

        self,

        subject
    ):

        connection = await self.client.connect()

        async def handler(message):

            payload = json.loads(

                message.data.decode()
            )

            print(

                f"[{message.subject}]",

                payload
            )

        await connection.subscribe(

            subject,

            cb=handler
        )

        return connection