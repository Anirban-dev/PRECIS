from datetime import datetime


class LatencyTracker:

    def latency(

        self,

        start_time,

        end_time
    ):

        return {

            "latency_ms":

                (end_time - start_time)
                * 1000,

            "timestamp":

                datetime.utcnow().isoformat()
        }