import numpy as np


class AbnormalMotion:

    def detect(

        self,

        velocity_vectors
    ):

        magnitudes = []

        for vector in velocity_vectors:

            magnitude = np.linalg.norm(
                vector
            )

            magnitudes.append(
                magnitude
            )

        if not magnitudes:

            return False

        average = np.mean(
            magnitudes
        )

        peak = np.max(
            magnitudes
        )

        return peak > average * 2