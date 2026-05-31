from datetime import datetime


class EmergencyService:

    def generate_response(

        self,

        risk_level,

        sector_id,

        sensor_health
    ):

        recommendations = {

            "LOW": [

                "Continue monitoring"
            ],

            "MEDIUM": [

                "Increase surveillance",

                "Prepare crowd control team"
            ],

            "HIGH": [

                "Open alternate routes",

                "Deploy security personnel"
            ],

            "CRITICAL": [

                "Immediate evacuation",

                "Activate emergency protocol",

                "Notify authorities"
            ]
        }

        return {

            "sector_id":
                sector_id,

            "risk_level":
                risk_level,

            "sensor_health":
                sensor_health,

            "actions":

                recommendations.get(
                    risk_level,
                    []
                ),

            "timestamp":
                datetime.utcnow().isoformat()
        }