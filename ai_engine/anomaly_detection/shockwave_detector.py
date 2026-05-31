import numpy as np


class ShockwaveDetector:

    def detect(

        self,

        density_history
    ):

        if len(density_history) < 5:

            return False

        gradient = np.gradient(
            density_history
        )

        max_change = max(

            abs(value)

            for value in gradient
        )

        return max_change > 8

    def score(

        self,

        density_history
    ):

        if len(density_history) < 5:

            return 0

        gradient = np.gradient(
            density_history
        )

        return float(

            np.max(
                np.abs(
                    gradient
                )
            )
        )