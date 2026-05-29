from datetime import datetime


class EventConsumer:

    def consume(

        self,

        payload
    ):

        return {

            "payload":
                payload,

            "consumed_at":
                datetime.utcnow().isoformat(),

            "status":
                "CONSUMED"
        }