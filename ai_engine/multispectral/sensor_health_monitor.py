from datetime import datetime


class SensorHealthMonitor:

    def evaluate(

        self,

        fps,

        frame_age,

        packet_loss
    ):

        health = "HEALTHY"

        if fps < 10:

            health = "DEGRADED"

        if frame_age > 3:

            health = "OFFLINE"

        if packet_loss > 30:

            health = "DEGRADED"

        return {

            "health":
                health,

            "fps":
                fps,

            "packet_loss":
                packet_loss,

            "frame_age":
                frame_age,

            "timestamp":
                datetime.utcnow().isoformat()
        }