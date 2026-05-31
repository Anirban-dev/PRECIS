import numpy as np


class OutstrokePredictor:

    def detect(

        self,

        trajectory_vectors
    ):

        if len(trajectory_vectors) < 3:

            return False

        vectors = np.array(
            trajectory_vectors
        )

        magnitude = np.linalg.norm(

            vectors,

            axis=1
        )

        sudden_change = np.max(
            magnitude
        )

        return sudden_change > 25

    def score(

        self,

        trajectory_vectors
    ):

        if len(trajectory_vectors) == 0:

            return 0

        vectors = np.array(
            trajectory_vectors
        )

        magnitude = np.linalg.norm(

            vectors,

            axis=1
        )

        return float(
            np.max(magnitude)
        )