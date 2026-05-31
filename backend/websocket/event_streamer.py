from datetime import datetime


class EventStreamer:

    def create_event(

        self,

        event_type,

        payload,

        camera_type,

        sector_id
    ):

        return {

            "event_type":
                event_type,

            "camera_type":
                camera_type,

            "sector_id":
                sector_id,

            "payload":
                payload,

            "timestamp":
                datetime.utcnow().isoformat()
        }