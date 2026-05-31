import numpy as np


class TurbulenceForecaster:

    def forecast(

        self,

        turbulence_history
    ):

        if len(turbulence_history) < 3:

            return 0

        trend = np.polyfit(

            range(
                len(
                    turbulence_history
                )
            ),

            turbulence_history,

            1
        )

        future_value = (

            turbulence_history[-1]

            +

            trend[0]
        )

        return round(

            float(
                future_value
            ),

            2
        )