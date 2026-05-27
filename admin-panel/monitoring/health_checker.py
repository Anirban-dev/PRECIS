from datetime import datetime


class HealthChecker:

    def check_services(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "gateway": "ONLINE",

            "cv_engine": "ONLINE",

            "database": "ONLINE",

            "websocket": "ONLINE"
        }