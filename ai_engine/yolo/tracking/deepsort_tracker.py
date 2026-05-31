from deep_sort_realtime.deepsort_tracker import DeepSort


class DeepSortTracker:

    def __init__(self):

        self.tracker = DeepSort(

            max_age=30,

            n_init=3,

            max_cosine_distance=0.4
        )

    def track(

        self,

        detections
    ):

        tracks = self.tracker.update_tracks(

            detections,

            frame=None
        )

        results = []

        for track in tracks:

            if not track.is_confirmed():

                continue

            results.append({

                "track_id":
                    track.track_id,

                "bbox":
                    track.to_ltrb().tolist()
            })

        return results

    def track_multispectral(

        self,

        rgb_detections,

        thermal_detections,

        infrared_detections
    ):

        fused = (

            rgb_detections +

            thermal_detections +

            infrared_detections
        )

        return self.track(
            fused
        )