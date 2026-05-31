from datetime import datetime


class IncidentService:

    def create_incident(

        self,

        sector_id,

        risk_level,

        source
    ):

        return {

            "incident_id":

                f"INC-{datetime.utcnow().timestamp()}",

            "sector_id":
                sector_id,

            "risk_level":
                risk_level,

            "source":
                source,

            "created_at":
                datetime.utcnow().isoformat()
        }