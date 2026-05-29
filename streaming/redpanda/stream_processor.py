from datetime import datetime


class StreamProcessor:

    def process(
        self,
        payload
    ):

        return {
            "processed_payload": payload,
            "processed_at":
                datetime.utcnow().isoformat()
        }