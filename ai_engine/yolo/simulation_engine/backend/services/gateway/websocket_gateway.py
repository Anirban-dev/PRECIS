from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import logging
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "websocket-gateway"
)


class ConnectionManager:

    def __init__(self):

        self.active_connections = []

        logger.info(
            "Initializing WebSocket Gateway..."
        )

    async def connect(

        self,

        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

        logger.info(
            f"New dashboard connected. "
            f"Active connections: "
            f"{len(self.active_connections)}"
        )

    def disconnect(

        self,

        websocket: WebSocket
    ):

        self.active_connections.remove(
            websocket
        )

        logger.info(
            f"Dashboard disconnected. "
            f"Active connections: "
            f"{len(self.active_connections)}"
        )

    async def send_personal_message(

        self,

        message,

        websocket: WebSocket
    ):

        await websocket.send_text(

            json.dumps(message)
        )

    async def broadcast(

        self,

        message
    ):

        disconnected_clients = []

        for connection in self.active_connections:

            try:

                await connection.send_text(

                    json.dumps(message)
                )

            except Exception:

                disconnected_clients.append(
                    connection
                )

        for client in disconnected_clients:

            self.disconnect(client)

        logger.info(

            f"[WEBSOCKET BROADCAST] "

            f"Delivered to "

            f"{len(self.active_connections)} clients"
        )


manager = ConnectionManager()


async def websocket_endpoint(

    websocket: WebSocket
):

    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            logger.info(

                f"[WEBSOCKET MESSAGE] "

                f"{data}"
            )

            response = {

                "timestamp":
                    datetime.utcnow().isoformat(),

                "system":
                    "PRECIS",

                "message":
                    "Real-time crowd intelligence active.",

                "received":
                    data
            }

            await manager.send_personal_message(

                response,

                websocket
            )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        logger.warning(
            "Dashboard client disconnected."
        )


async def broadcast_risk_update(

    risk_level,

    crowd_state,

    fusion_score
):

    payload = {

        "event": "risk_update",

        "timestamp":
            datetime.utcnow().isoformat(),

        "risk_level":
            risk_level,

        "crowd_state":
            crowd_state,

        "fusion_score":
            fusion_score
    }

    await manager.broadcast(payload)


async def broadcast_emergency_alert(

    location,

    risk_level,

    responders
):

    payload = {

        "event": "emergency_alert",

        "timestamp":
            datetime.utcnow().isoformat(),

        "location":
            location,

        "risk_level":
            risk_level,

        "responders":
            responders
    }

    await manager.broadcast(payload)


async def broadcast_live_analytics(

    turbulence_score,

    resonance_probability,

    shockwave_detected
):

    payload = {

        "event": "live_analytics",

        "timestamp":
            datetime.utcnow().isoformat(),

        "turbulence_score":
            turbulence_score,

        "resonance_probability":
            resonance_probability,

        "shockwave_detected":
            shockwave_detected
    }

    await manager.broadcast(payload)