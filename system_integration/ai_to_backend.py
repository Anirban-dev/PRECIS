from backend.services.notification_service import NotificationService


class AIToBackend:

    def __init__(self):

        self.notification = NotificationService()

    def send_alert(

        self,

        risk_level,

        message
    ):

        return self.notification.broadcast_alert(

            risk_level,

            message
        )