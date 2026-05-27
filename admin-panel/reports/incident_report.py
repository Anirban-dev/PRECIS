from datetime import datetime


class IncidentReport:

    def generate_report(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "incident_id": "INC-2045",

            "risk_level": "SEVERE",

            "affected_zones": 3
        }