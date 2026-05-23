from datetime import datetime
import logging
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "emergency-service"
)


class EmergencyService:

    def __init__(self):

        logger.info(
            "Initializing Emergency Coordination Service..."
        )

    def dispatch_emergency(

        self,

        risk_report,

        location="Unknown Zone"
    ):

        logger.info(
            "Processing emergency dispatch..."
        )

        risk_level = risk_report.get(
            "risk_level",
            "LOW"
        )

        responders = []

        if risk_level == "HIGH":

            responders.extend([

                "Venue Security",

                "Crowd Response Unit"
            ])

        elif risk_level == "SEVERE":

            responders.extend([

                "Police Response Team",

                "Rapid Rescue Unit",

                "Ambulance Dispatch"
            ])

        elif risk_level == "CRITICAL":

            responders.extend([

                "Disaster Response Force",

                "Police Command Center",

                "Emergency Ambulance Network",

                "Nearby Hospitals",

                "Fire Brigade"
            ])

        emergency_id = (
            f"EMG-"
            f"{random.randint(1000,9999)}"
        )

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "emergency_id":
                emergency_id,

            "location":
                location,

            "risk_level":
                risk_level,

            "responders":
                responders,

            "dispatch_status":
                "ACTIVE"
        }

        logger.info(

            f"[EMERGENCY] "

            f"Risk={risk_level} | "

            f"Location={location}"
        )

        return report


if __name__ == "__main__":

    risk_report = {

        "risk_level": "CRITICAL"
    }

    service = EmergencyService()

    result = service.dispatch_emergency(

        risk_report,

        "Gate A"
    )

    print(result)