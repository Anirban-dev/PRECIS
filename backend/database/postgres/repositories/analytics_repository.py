class AnalyticsRepository:

    def save_analytics(

        self,

        payload
    ):

        return {

            "status":
                "SAVED",

            "payload":
                payload
        }

    def fetch_analytics(self):

        return []