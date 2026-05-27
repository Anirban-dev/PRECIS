from datetime import datetime


class CrowdAnalytics:

    def crowd_metrics(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "crowd_density": 8.2,

            "active_zones": 5,

            "movement_velocity": 2.8
        }