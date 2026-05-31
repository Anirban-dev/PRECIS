import numpy as np


class TrajectoryAnomalyDetector:

    def detect(

        self,

        trajectory_points
    ):

        if len(trajectory_points) < 3:

            return False

        points = np.array(
            trajectory_points
        )

        velocity = np.diff(

            points,

            axis=0
        )

        acceleration = np.diff(

            velocity,

            axis=0
        )

        score = np.mean(

            np.abs(
                acceleration
            )
        )

        return score > 15