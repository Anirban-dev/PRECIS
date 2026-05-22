import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "notification-service"
)


class NotificationService:

    def __init__(self):

        logger.info(
            "Initializing Emergency Notification Service..."
        )

    def send_notifications(

        self,

        risk_report,

        dashboard_payload=None
    ):

        logger.info(
            "Processing emergency notifications..."
        )

        risk_level = risk_report.get(
            "risk_level",
            "LOW"
        )

        emergency_dispatch_required = (
            risk_report.get(
                "emergency_dispatch_required",
                False
            )
        )

        system_state = risk_report.get(
            "system_state",
            "STABLE"
        )

        notifications_sent = []

        if risk_level == "HIGH":

            notifications_sent.extend([

                {
                    "recipient":
                        "Crowd Monitoring Team",

                    "priority":
                        "MEDIUM",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Venue Security",

                    "priority":
                        "MEDIUM",

                    "status":
                        "SENT"
                }
            ])

        elif risk_level == "SEVERE":

            notifications_sent.extend([

                {
                    "recipient":
                        "Police Control Room",

                    "priority":
                        "HIGH",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Emergency Rescue Team",

                    "priority":
                        "HIGH",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Ambulance Network",

                    "priority":
                        "HIGH",

                    "status":
                        "SENT"
                }
            ])

        elif risk_level == "CRITICAL":

            notifications_sent.extend([

                {
                    "recipient":
                        "Police Command Center",

                    "priority":
                        "CRITICAL",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Nearby Hospitals",

                    "priority":
                        "CRITICAL",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Fire Brigade",

                    "priority":
                        "CRITICAL",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Rapid Response Force",

                    "priority":
                        "CRITICAL",

                    "status":
                        "SENT"
                },

                {
                    "recipient":
                        "Emergency Ambulance Dispatch",

                    "priority":
                        "CRITICAL",

                    "status":
                        "SENT"
                }
            ])

        live_dashboard_alert = None

        if dashboard_payload:

            live_dashboard_alert = {

                "alert_status":
                    dashboard_payload.get(
                        "dashboard_status",
                        {}
                    ).get(
                        "alert_status",
                        "NORMAL"
                    ),

                "ui_color":
                    dashboard_payload.get(
                        "dashboard_status",
                        {}
                    ).get(
                        "ui_color",
                        "green"
                    )
            }

        emergency_mode = False

        if emergency_dispatch_required:

            emergency_mode = True

        estimated_response_time = "N/A"

        if risk_level == "HIGH":

            estimated_response_time = (
                "5-10 minutes"
            )

        elif risk_level == "SEVERE":

            estimated_response_time = (
                "3-5 minutes"
            )

        elif risk_level == "CRITICAL":

            estimated_response_time = (
                "1-3 minutes"
            )

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "risk_level":
                risk_level,

            "system_state":
                system_state,

            "emergency_mode":
                emergency_mode,

            "estimated_response_time":
                estimated_response_time,

            "notifications_sent":
                notifications_sent,

            "live_dashboard_alert":
                live_dashboard_alert
        }

        logger.info(

            f"[NOTIFICATION SERVICE] "

            f"Risk={risk_level} | "

            f"Notifications={len(notifications_sent)} | "

            f"EmergencyMode={emergency_mode}"
        )

        return report


if __name__ == "__main__":

    risk_report = {

        "risk_level": "CRITICAL",

        "system_state": "PRE_DISASTER",

        "emergency_dispatch_required": True
    }

    dashboard_payload = {

        "dashboard_status": {

            "alert_status":
                "CRITICAL_ALERT",

            "ui_color":
                "red"
        }
    }

    try:

        service = NotificationService()

        result = service.send_notifications(

            risk_report,

            dashboard_payload
        )

        print(
            "\n========== NOTIFICATION REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Notification Service Error: {e}"
        )