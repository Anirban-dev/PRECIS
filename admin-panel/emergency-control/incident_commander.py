from datetime import datetime


class IncidentCommander:

    def incident_status(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "incident_level": "CRITICAL",

            "zones_locked": 2,

            "medical_support_active": True
        }