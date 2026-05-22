# cv_engine/event_publisher.py

import json
import logging
from datetime import datetime

# =========================================================
# OPTIONAL NATS IMPORT
# =========================================================

try:

    from nats.aio.client import Client as NATS

    NATS_AVAILABLE = True

except ImportError:

    NATS_AVAILABLE = False

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("event-publisher")

# =========================================================
# EVENT PUBLISHER ENGINE
# =========================================================

class EventPublisher:

    def __init__(

        self,

        nats_server="nats://localhost:4222"
    ):

        self.nats_server = nats_server

        self.nc = None

        logger.info(
            "Initializing Event Publisher Engine..."
        )

    # =====================================================
    # CONNECT TO NATS
    # =====================================================

    async def connect(self):

        if not NATS_AVAILABLE:

            logger.warning(
                "NATS client not installed. "
                "Running in simulation mode."
            )

            return False

        try:

            self.nc = NATS()

            await self.nc.connect(
                servers=[self.nats_server]
            )

            logger.info(
                f"Connected to NATS server: "
                f"{self.nats_server}"
            )

            return True

        except Exception as e:

            logger.error(
                f"NATS connection failed: {e}"
            )

            return False

    # =====================================================
    # PUBLISH EVENT
    # =====================================================

    async def publish_event(

        self,

        subject,

        payload
    ):

        """
        Publish crowd intelligence events
        to the distributed event bus.
        """

        event = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "subject":
                subject,

            "payload":
                payload
        }

        event_json = json.dumps(event)

        # -------------------------------------------------
        # SIMULATION MODE
        # -------------------------------------------------

        if not NATS_AVAILABLE or self.nc is None:

            logger.info(

                f"[SIMULATED EVENT] "

                f"Subject={subject} | "

                f"Payload={event_json}"
            )

            return {

                "status": "simulated",

                "subject": subject
            }

        # -------------------------------------------------
        # REAL NATS PUBLISH
        # -------------------------------------------------

        try:

            await self.nc.publish(

                subject,

                event_json.encode()
            )

            logger.info(

                f"[EVENT PUBLISHED] "

                f"Subject={subject}"
            )

            return {

                "status": "published",

                "subject": subject
            }

        except Exception as e:

            logger.error(
                f"Event publish failed: {e}"
            )

            return {

                "status": "failed",

                "error": str(e)
            }

    # =====================================================
    # CROWD RISK EVENT
    # =====================================================

    async def publish_risk_event(

        self,

        risk_report
    ):

        risk_level = risk_report.get(
            "risk_level",
            "UNKNOWN"
        )

        subject = (
            f"precis.crowd.risk.{risk_level.lower()}"
        )

        return await self.publish_event(

            subject,

            risk_report
        )

    # =====================================================
    # EMERGENCY ALERT EVENT
    # =====================================================

    async def publish_emergency_alert(

        self,

        outstroke_report
    ):

        subject = (
            "precis.emergency.outstroke"
        )

        return await self.publish_event(

            subject,

            outstroke_report
        )

    # =====================================================
    # RESONANCE EVENT
    # =====================================================

    async def publish_resonance_event(

        self,

        resonance_metrics
    ):

        subject = (
            "precis.crowd.resonance"
        )

        return await self.publish_event(

            subject,

            resonance_metrics
        )

    # =====================================================
    # CLOSE CONNECTION
    # =====================================================

    async def close(self):

        if self.nc is not None:

            await self.nc.close()

            logger.info(
                "NATS connection closed."
            )

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    import asyncio

    logger.info(
        "Running Event Publisher self-test..."
    )

    async def run_test():

        publisher = EventPublisher()

        await publisher.connect()

        # -------------------------------------------------
        # SYNTHETIC TEST DATA
        # -------------------------------------------------

        risk_report = {

            "risk_level": "CRITICAL",

            "crowd_criticality_index": 9.4,

            "shockwave_detected": True
        }

        outstroke_report = {

            "outstroke_risk": "CRITICAL",

            "outstroke_probability": 0.92,

            "early_warning": True
        }

        resonance_metrics = {

            "resonance_score": 8.7,

            "resonance_probability": 0.91
        }

        # -------------------------------------------------
        # PUBLISH EVENTS
        # -------------------------------------------------

        await publisher.publish_risk_event(
            risk_report
        )

        await publisher.publish_emergency_alert(
            outstroke_report
        )

        await publisher.publish_resonance_event(
            resonance_metrics
        )

        # -------------------------------------------------
        # CLOSE CONNECTION
        # -------------------------------------------------

        await publisher.close()

    asyncio.run(run_test())