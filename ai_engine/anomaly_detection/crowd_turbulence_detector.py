import numpy as np


class CrowdTurbulenceDetector:

    def calculate_turbulence(

        self,

        flow_vectors
    ):

        if len(flow_vectors) == 0:

            return 0.0

        vectors = np.array(
            flow_vectors
        )

        magnitude = np.linalg.norm(

            vectors,

            axis=1
        )

        return float(

            np.std(
                magnitude
            )
        )

    def classify(

        self,

        turbulence
    ):

        if turbulence >= 15:

            return "CRITICAL"

        if turbulence >= 10:

            return "HIGH"

        if turbulence >= 5:

            return "MEDIUM"

        return "LOW"