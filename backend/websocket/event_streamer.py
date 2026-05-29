from datetime import datetime


class EventStreamer:

    def build_event(

        self,

        event_type,

        payload
    ):

        return {

            "event_type":
                event_type,

            "payload":
                payload,

            "timestamp":
                datetime.utcnow().isoformat()
        }