from datetime import datetime
import logging

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
            "Initializing Notification Service..."
        )

    def send_notifications(

        self,

        emergency_report
    ):

        logger.info(
            "Sending emergency notifications..."
        )

        responders = emergency_report.get(
            "responders",
            []
        )

        notifications = []

        for responder in responders:

            notifications.append({

                "recipient":
                    responder,

                "status":
                    "DELIVERED"
            })

        result = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "notifications_sent":
                len(notifications),

            "delivery_status":
                "SUCCESS",

            "notifications":
                notifications
        }

        logger.info(

            f"[NOTIFICATIONS] "

            f"Sent={len(notifications)}"
        )

        return result


if __name__ == "__main__":

    emergency_report = {

        "responders": [

            "Police Command Center",

            "Fire Brigade",

            "Emergency Ambulance Network"
        ]
    }

    service = NotificationService()

    result = service.send_notifications(
        emergency_report
    )

    print(result)