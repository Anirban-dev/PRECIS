import numpy as np


class PanicWaveTracker:

    def detect(

        self,

        density_history
    ):

        if len(density_history) < 5:

            return False

        gradient = np.gradient(
            density_history
        )

        return np.max(
            np.abs(
                gradient
            )
        ) > 6

    def intensity(

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