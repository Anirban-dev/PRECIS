from datetime import datetime


class AlertService:

    def create_alert(
        self,
        camera_id,
        risk_level
    ):

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "camera_id": camera_id,
            "risk_level": risk_level,
            "message": f"{risk_level} risk crowd alert"
        }