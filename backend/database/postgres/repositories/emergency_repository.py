class EmergencyRepository:

    def save_emergency(

        self,

        payload
    ):

        return {

            "status":
                "SAVED",

            "payload":
                payload
        }

    def get_emergencies(self):

        return []