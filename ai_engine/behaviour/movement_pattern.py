import numpy as np


class MovementPattern:

    def analyze(

        self,

        trajectories
    ):

        speeds = []

        for trajectory in trajectories:

            if len(trajectory) < 2:

                continue

            start = trajectory[0]

            end = trajectory[-1]

            distance = np.linalg.norm(

                np.array(end) -

                np.array(start)
            )

            speeds.append(distance)

        if not speeds:

            return "STATIC"

        average_speed = np.mean(
            speeds
        )

        if average_speed > 120:

            return "CHAOTIC"

        if average_speed > 60:

            return "FAST_FLOW"

        return "NORMAL_FLOW"