from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "alert-dispatcher"
)


class AlertDispatcher:

    def __init__(self):

        logger.info(
            "Initializing Alert Dispatcher..."
        )

    def dispatch_alert(

        self,

        risk_report
    ):

        risk_level = risk_report.get(
            "risk_level",
            "LOW"
        )

        responders = []

        if risk_level == "HIGH":

            responders.extend([

                "Security Team",

                "Crowd Control Unit"
            ])

        elif risk_level == "SEVERE":

            responders.extend([

                "Police Response",

                "Ambulance Team",

                "Emergency Rescue Unit"
            ])

        elif risk_level == "CRITICAL":

            responders.extend([

                "Police Command",

                "Disaster Response Force",

                "Nearby Hospitals",

                "Fire Brigade"
            ])

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "risk_level":
                risk_level,

            "responders":
                responders,

            "dispatch_status":
                "ACTIVE"
        }

        logger.info(

            f"[ALERT] "

            f"Risk={risk_level}"
        )

        return report