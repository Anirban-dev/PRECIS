import json

from streaming.nats.nats_client import NATSClient


class NATSPublisher:

    def __init__(self):

        self.client = NATSClient()

    async def publish(

        self,

        subject,

        payload
    ):

        connection = await self.client.connect()

        await connection.publish(

            subject,

            json.dumps(payload).encode()
        )

        await connection.flush()

        await self.client.disconnect()

        return {

            "subject": subject,

            "status": "PUBLISHED"
        }