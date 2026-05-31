class ByteTrackTracker:

    def __init__(self):

        self.active_tracks = {}

    def update(

        self,

        detections
    ):

        tracked = []

        for index, detection in enumerate(
            detections
        ):

            tracked.append({

                "track_id":
                    index,

                "bbox":
                    detection["bbox"],

                "confidence":
                    detection["confidence"]
            })

        return tracked

    def update_multispectral(

        self,

        rgb_detections,

        thermal_detections,

        infrared_detections
    ):

        detections = (

            rgb_detections +

            thermal_detections +

            infrared_detections
        )

        return self.update(
            detections
        )