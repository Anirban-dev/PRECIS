from datetime import datetime


class StreamMonitor:

    def monitor_streams(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "active_streams": 6,

            "offline_streams": 1,

            "latency_ms": 120
        }