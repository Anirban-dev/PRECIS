import numpy as np


class DensityAnomalyDetector:

    def detect(

        self,

        density_map
    ):

        density = np.array(
            density_map
        )

        mean_density = np.mean(
            density
        )

        anomaly_regions = []

        for index, value in enumerate(
            density
        ):

            if value > mean_density * 1.5:

                anomaly_regions.append(
                    index
                )

        return anomaly_regions