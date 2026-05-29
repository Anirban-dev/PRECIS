from backend.websocket.websocket_manager import (
    WebSocketManager
)


class LiveBroadcast:

    def __init__(self):

        self.manager = WebSocketManager()

    async def send_event(

        self,

        event
    ):

        await self.manager.broadcast(
            event
        )