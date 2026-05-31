from fastapi import WebSocket


class WebSocketManager:

    def __init__(self):

        self.connections = []

    async def connect(

        self,

        websocket: WebSocket
    ):

        await websocket.accept()

        self.connections.append(
            websocket
        )

    def disconnect(

        self,

        websocket
    ):

        if websocket in self.connections:

            self.connections.remove(
                websocket
            )

    async def broadcast(

        self,

        payload
    ):

        disconnected = []

        for connection in self.connections:

            try:

                await connection.send_json(
                    payload
                )

            except Exception:

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect(
                connection
            )