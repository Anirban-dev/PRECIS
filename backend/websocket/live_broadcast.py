from collections import defaultdict


class LiveBroadcast:

    def __init__(self):

        self.channels = defaultdict(list)

    def subscribe(

        self,

        channel,

        websocket
    ):

        self.channels[channel].append(
            websocket
        )

    async def broadcast(

        self,

        channel,

        payload
    ):

        connections = self.channels.get(
            channel,
            []
        )

        for websocket in connections:

            try:

                await websocket.send_json(
                    payload
                )

            except Exception:

                pass