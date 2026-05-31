import numpy as np


class CrowdResonanceDetector:

    def calculate(

        self,

        motion_vectors
    ):

        if len(motion_vectors) == 0:

            return 0

        vectors = np.array(
            motion_vectors
        )

        coherence = np.mean(

            np.linalg.norm(

                vectors,

                axis=1
            )
        )

        return float(
            coherence
        )

    def classify(

        self,

        score
    ):

        if score > 25:

            return "HIGH"

        if score > 15:

            return "MEDIUM"

        return "LOW"