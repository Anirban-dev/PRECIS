from datetime import datetime
import numpy as np


class AnalyticsService:

    def generate_crowd_analytics(

        self,

        rgb_density,

        thermal_density,

        infrared_density
    ):

        rgb_mean = float(
            np.mean(rgb_density)
        )

        thermal_mean = float(
            np.mean(thermal_density)
        )

        infrared_mean = float(
            np.mean(infrared_density)
        )

        overall_density = (

            rgb_mean * 0.4 +

            thermal_mean * 0.35 +

            infrared_mean * 0.25
        )

        return {

            "rgb_density":
                rgb_mean,

            "thermal_density":
                thermal_mean,

            "infrared_density":
                infrared_mean,

            "overall_density":
                round(
                    overall_density,
                    2
                ),

            "generated_at":
                datetime.utcnow().isoformat()
        }