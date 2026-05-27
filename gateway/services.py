from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "gateway-service"
)


class GatewayService:

    def __init__(self):

        logger.info(
            "Initializing Gateway Service..."
        )

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
                payload
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
                payload
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
                payload
        }