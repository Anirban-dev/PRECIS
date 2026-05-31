from backend.services.notification_service import (
    NotificationService
)


class AlertWorker:

    def __init__(self):

        self.notification = (
            NotificationService()
        )

    def process(

        self,

        risk_event
    ):

        return self.notification.broadcast_alert(

            risk_event["risk_level"],

            risk_event
        )