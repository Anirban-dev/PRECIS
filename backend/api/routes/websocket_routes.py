from fastapi import (
    APIRouter,
    WebSocket
)

from backend.websocket.websocket_manager import (
    WebSocketManager
)

router = APIRouter()

manager = WebSocketManager()


@router.websocket("/stream")

async def websocket_stream(

    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except Exception:

        manager.disconnect(
            websocket
        )