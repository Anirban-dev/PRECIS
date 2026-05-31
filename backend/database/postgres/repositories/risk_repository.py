class RiskRepository:

    def save_risk_event(

        self,

        payload
    ):

        return {

            "status":
                "SAVED",

            "payload":
                payload
        }

    def get_recent_events(self):

        return []