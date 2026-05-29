from datetime import datetime


class StreamHealth:

    def status(self):

        return {

            "service":
                "streaming",

            "status":
                "HEALTHY",

            "timestamp":
                datetime.utcnow().isoformat()
        }