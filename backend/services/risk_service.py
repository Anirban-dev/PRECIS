import numpy as np


class RiskService:

    def calculate_density_score(

        self,

        density_map
    ):

        return float(
            np.mean(density_map)
        )

    def calculate_sensor_score(

        self,

        confidence,

        sensor_health
    ):

        score = confidence * 100

        if sensor_health == "DEGRADED":

            score *= 0.8

        elif sensor_health == "OFFLINE":

            score *= 0.5

        return score

    def calculate_risk(

        self,

        density_map,

        turbulence_score,

        fusion_confidence,

        sensor_health
    ):

        density_score = (

            self.calculate_density_score(
                density_map
            )
        )

        sensor_score = (

            self.calculate_sensor_score(

                fusion_confidence,

                sensor_health
            )
        )

        risk_score = (

            density_score * 0.45 +

            turbulence_score * 0.40 +

            sensor_score * 0.15
        )

        if risk_score >= 85:

            risk_level = "CRITICAL"

        elif risk_score >= 70:

            risk_level = "HIGH"

        elif risk_score >= 50:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        return {

            "risk_score":
                round(risk_score, 2),

            "risk_level":
                risk_level,

            "sensor_health":
                sensor_health,

            "fusion_confidence":
                fusion_confidence
        }