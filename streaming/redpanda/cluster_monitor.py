from datetime import datetime


class ClusterMonitor:

    def health(self):

        return {

            "cluster":
                "redpanda",

            "status":
                "ACTIVE",

            "timestamp":
                datetime.utcnow().isoformat()
        }