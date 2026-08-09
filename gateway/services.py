from datetime import datetime
import logging
import os

import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "gateway-service"
)


class GatewayService:

    def __init__(self):
        self.backend_url = os.getenv(
            "PRECIS_BACKEND_URL",
            "http://127.0.0.1:8000"
        ).rstrip("/")

        logger.info(
            "Initializing Gateway Service..."
        )

    def _forward(self, path, payload):
        try:
            with httpx.Client(timeout=3.0) as client:
                response = client.post(f"{self.backend_url}{path}", json=payload)
                response.raise_for_status()
                return {
                    "forwarded": True,
                    "status_code": response.status_code,
                    "response": response.json()
                }
        except httpx.HTTPError as exc:
            logger.warning("Backend forwarding failed for %s: %s", path, exc)
            return {
                "forwarded": False,
                "error": str(exc)
            }

    def process_event(

        self,

        payload
    ):

        logger.info(
            f"Processing event: {payload}"
        )

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "type":
                "event",

            "status":
                "processed",

            "payload":
                payload,

            "backend":
                self._forward("/analytics/crowd", payload)
                if all(k in payload for k in ("rgb_density", "thermal_density", "infrared_density"))
                else {"forwarded": False, "reason": "No matching backend event endpoint"}
        }

    def process_risk(

        self,

        payload
    ):

        logger.info(
            f"Processing risk: {payload}"
        )

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "type":
                "risk",

            "status":
                "processed",

            "payload":
                payload,

            "backend":
                self._forward(
                    "/risk/",
                    {
                        "density_map": [payload.get("crowd_density", 0)],
                        "turbulence_score": payload.get("turbulence_score", 0),
                        "fusion_confidence": 0.95,
                        "sensor_health": "HEALTHY"
                    }
                )
        }

    def process_alert(

        self,

        payload
    ):

        logger.info(
            f"Processing alert: {payload}"
        )

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "type":
                "alert",

            "status":
                "processed",

            "payload":
                payload,

            "backend":
                {"forwarded": False, "reason": "Alert persistence endpoint is not implemented in backend"}
        }
