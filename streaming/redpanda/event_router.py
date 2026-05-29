class EventRouter:

    def route(
        self,
        event_type
    ):

        routes = {

            "risk":
                "risk-events",

            "analytics":
                "analytics-events",

            "emergency":
                "emergency-events"
        }

        return routes.get(
            event_type,
            "general-events"
        )