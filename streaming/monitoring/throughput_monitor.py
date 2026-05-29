from datetime import datetime


class ThroughputMonitor:

    def calculate(

        self,

        total_events,

        duration
    ):

        throughput = 0

        if duration > 0:

            throughput = total_events / duration

        return {

            "throughput":
                throughput,

            "timestamp":
                datetime.utcnow().isoformat()
        }