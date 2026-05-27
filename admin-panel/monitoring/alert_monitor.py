from datetime import datetime


class AlertMonitor:

    def active_alerts(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "critical_alerts": 1,

            "high_alerts": 3,

            "moderate_alerts": 5
        }