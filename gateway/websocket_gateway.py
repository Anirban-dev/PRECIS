from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "websocket-gateway"
)

websocket_router = APIRouter()


class ConnectionManager:

    def __init__(self):

        self.active_connections = []

    async def connect(

        self,

        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

        logger.info(
            "WebSocket client connected."
        )

    def disconnect(

        self,

        websocket: WebSocket
    ):

        self.active_connections.remove(
            websocket
        )

        logger.info(
            "WebSocket client disconnected."
        )

    async def broadcast(

        self,

        message: str
    ):

        for connection in self.active_connections:

            await connection.send_text(
                message
            )


manager = ConnectionManager()


@websocket_router.websocket("/ws/live")

async def websocket_endpoint(

    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            data = await websocket.receive_text()

            logger.info(
                f"WebSocket Data: {data}"
            )

            await manager.broadcast(
                f"Broadcast: {data}"
            )

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )