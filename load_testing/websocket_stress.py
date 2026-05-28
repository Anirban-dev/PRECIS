import asyncio
import websockets


async def stress():

    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri):

        while True:

            await asyncio.sleep(0.01)


asyncio.run(stress())