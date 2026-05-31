class EmergencyRecommendationEngine:

    def recommend(

        self,

        risk_level,

        sector_id
    ):

        actions = {

            "LOW": [

                "Continue Monitoring"
            ],

            "MEDIUM": [

                "Increase Surveillance",

                "Prepare Security Teams"
            ],

            "HIGH": [

                "Open Alternative Routes",

                "Deploy Crowd Marshals",

                "Increase Announcements"
            ],

            "CRITICAL": [

                "Immediate Evacuation",

                "Activate Emergency Teams",

                "Notify Authorities",

                "Open All Emergency Exits"
            ]
        }

        return {

            "sector_id":
                sector_id,

            "risk_level":
                risk_level,

            "recommended_actions":

                actions.get(
                    risk_level,
                    []
                )
        }