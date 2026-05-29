from nats.aio.client import Client as NATS


class NATSClient:

    def __init__(self):

        self.client = NATS()

    async def connect(self):

        await self.client.connect(
            servers=[
                "nats://localhost:4222"
            ]
        )

        return self.client

    async def disconnect(self):

        if self.client.is_connected:

            await self.client.close()