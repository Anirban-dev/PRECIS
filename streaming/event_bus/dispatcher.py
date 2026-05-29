class EventDispatcher:

    def dispatch(
        self,
        event
    ):

        return {

            "event":
                event,

            "status":
                "DISPATCHED"
        }