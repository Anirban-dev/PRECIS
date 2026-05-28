class TrackManager:

    def __init__(self):

        self.active_tracks = {}

    def update_track(

        self,

        track_id,

        bbox
    ):

        self.active_tracks[
            track_id
        ] = bbox

    def fetch_tracks(self):

        return self.active_tracks