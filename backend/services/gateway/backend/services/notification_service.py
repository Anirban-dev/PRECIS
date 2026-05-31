from datetime import datetime


class NotificationService:

    def broadcast_alert(

        self,

        risk_level,

        payload
    ):

        return {

            "risk_level":
                risk_level,

            "payload":
                payload,

            "sent_at":
                datetime.utcnow().isoformat(),

            "status":
                "DELIVERED"
        }

    def multispectral_alert(

        self,

        camera_type,

        sensor_health,

        message
    ):

        return {

            "camera_type":
                camera_type,

            "sensor_health":
                sensor_health,

            "message":
                message,

            "status":
                "SENT"
        }