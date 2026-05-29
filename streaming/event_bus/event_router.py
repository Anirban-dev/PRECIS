class EventRouter:

    def route(
        self,
        event_type
    ):

        mapping = {

            "risk":
                "risk-channel",

            "alert":
                "alert-channel",

            "analytics":
                "analytics-channel"
        }

        return mapping.get(
            event_type,
            "default-channel"
        )