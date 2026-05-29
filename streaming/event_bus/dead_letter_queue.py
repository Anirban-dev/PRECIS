class DeadLetterQueue:

    def move(
        self,
        payload
    ):

        return {

            "payload":
                payload,

            "queue":
                "DLQ",

            "status":
                "STORED"
        }