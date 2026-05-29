from backend.websocket.websocket_manager import WebSocketManager


class BackendToWebSocket:

    def __init__(self):

        self.manager = WebSocketManager()

    async def emit(

        self,

        payload
    ):

        await self.manager.broadcast(
            payload
        )