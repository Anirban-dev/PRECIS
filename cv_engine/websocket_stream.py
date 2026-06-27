import asyncio
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "websocket-stream"
)


class WebSocketStream:

    def __init__(self):

        logger.info(
            "Initializing WebSocket Stream..."
        )

    async def broadcast(

        self,

        payload
    ):

        message = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "payload":
                payload
        }

        logger.info(

            f"[WEBSOCKET STREAM] "

            f"{json.dumps(message)}"
        )

        await asyncio.sleep(1)

        return message