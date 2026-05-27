from datetime import datetime


class LiveAlertControl:

    def live_alerts(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "alerts_broadcasted": 7,

            "active_alert_channels": 4
        }