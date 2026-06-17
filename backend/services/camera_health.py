from datetime import datetime


class CameraHealth:

    def check(

        self,

        running: bool
    ):

        return {

            "healthy": running,

            "last_check":
                datetime.utcnow().isoformat()
        }