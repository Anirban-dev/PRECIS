from datetime import datetime


class EmergencyReport:

    def emergency_summary(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "critical_events": 2,

            "responders_dispatched": 16,

            "evacuations_completed": 1
        }