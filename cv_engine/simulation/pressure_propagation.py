import numpy as np


class PressurePropagation:

    def calculate(

        self,

        density_map
    ):

        density = np.array(
            density_map
        )

        gradients = np.gradient(
            density
        )

        pressure = np.sum(

            np.abs(
                gradients
            )
        )

        return float(
            pressure
        )

    def classify(

        self,

        pressure
    ):

        if pressure > 100:

            return "CRITICAL"

        if pressure > 50:

            return "HIGH"

        if pressure > 25:

            return "MEDIUM"

        return "LOW"