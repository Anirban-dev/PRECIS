class TrajectoryTracker:

    def __init__(self):

        self.trajectories = {}

    def update(

        self,

        track_id,

        point
    ):

        if track_id not in self.trajectories:

            self.trajectories[
                track_id
            ] = []

        self.trajectories[
            track_id
        ].append(point)

    def fetch_trajectory(

        self,

        track_id
    ):

        return self.trajectories.get(

            track_id,

            []
        )