class MultiCameraTracker:

    def merge_tracks(

        self,

        camera_tracks
    ):

        merged = []

        for tracks in camera_tracks:

            merged.extend(tracks)

        return merged