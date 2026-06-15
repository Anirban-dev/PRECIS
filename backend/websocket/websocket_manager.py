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

        print(
            f"WebSocket connected. Active connections: {len(self.connections)}"
        )

    def disconnect(

        self,

        websocket
    ):

        if websocket in self.connections:

            self.connections.remove(
                websocket
            )

            print(
                f"WebSocket disconnected. Active connections: {len(self.connections)}"
            )

    async def broadcast(

        self,

        payload
    ):

        print(
            "Broadcasting payload:",
            payload
        )

        disconnected = []

        for connection in self.connections:

            try:

                await connection.send_json(
                    payload
                )

            except Exception as e:

                print(
                    "Broadcast failed:",
                    str(e)
                )

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect(
                connection
            )