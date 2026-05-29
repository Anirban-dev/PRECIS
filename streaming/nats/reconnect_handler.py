import asyncio


class ReconnectHandler:

    async def reconnect(

        self,

        client,

        retries=5
    ):

        for attempt in range(retries):

            try:

                await client.connect()

                return True

            except Exception:

                await asyncio.sleep(2)

        return False