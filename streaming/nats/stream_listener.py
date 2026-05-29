from datetime import datetime


class StreamListener:

    def listen(

        self,

        stream_name
    ):

        return {

            "stream": stream_name,

            "started_at":
                datetime.utcnow().isoformat(),

            "status":
                "LISTENING"
        }