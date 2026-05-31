import numpy as np


class StampedePredictor:

    def predict(

        self,

        density_score,

        turbulence_score,

        pressure_score,

        panic_score
    ):

        risk = (

            density_score * 0.30 +

            turbulence_score * 0.25 +

            pressure_score * 0.25 +

            panic_score * 0.20
        )

        if risk >= 85:

            level = "CRITICAL"

        elif risk >= 70:

            level = "HIGH"

        elif risk >= 50:

            level = "MEDIUM"

        else:

            level = "LOW"

        return {

            "stampede_probability":

                round(
                    risk,
                    2
                ),

            "risk_level":
                level
        }