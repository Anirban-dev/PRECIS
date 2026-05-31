import numpy as np


class CrowdFlowSimulator:

    def simulate(

        self,

        density_map,

        flow_vectors,

        steps=10
    ):

        density = np.array(
            density_map
        )

        flow = np.array(
            flow_vectors
        )

        future_density = density.copy()

        for _ in range(steps):

            future_density = (

                future_density +

                np.mean(flow)
            )

        return future_density.tolist()

    def average_density(

        self,

        density_map
    ):

        return float(

            np.mean(
                density_map
            )
        )