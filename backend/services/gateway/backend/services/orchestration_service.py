class OrchestrationService:

    def orchestrate(

        self,

        analytics,

        risk,

        emergency
    ):

        return {

            "analytics":
                analytics,

            "risk":
                risk,

            "emergency":
                emergency,

            "status":
                "ORCHESTRATED"
        }