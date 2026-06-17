import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        logger.info(
            f"WebSocket connected. Active connections: {len(self.connections)}"
        )

    def disconnect(self, websocket):
        if websocket in self.connections:
            self.connections.remove(websocket)
            logger.info(
                f"WebSocket disconnected. Active connections: {len(self.connections)}"
            )

    async def broadcast(self, payload):
        logger.info(
            f"Broadcasting payload: {payload}"
        )

        disconnected = []
        for connection in self.connections:
            try:
                await connection.send_json(payload)
            except Exception as e:
                logger.error(
                    f"Broadcast failed: {str(e)}"
                )
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)
