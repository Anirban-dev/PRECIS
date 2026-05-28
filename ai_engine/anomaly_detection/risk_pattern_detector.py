class RiskPatternDetector:

    def evaluate(

        self,

        anomaly_score,

        crowd_density
    ):

        risk = (

            anomaly_score * 0.6 +

            crowd_density * 0.4
        )

        if risk > 8:

            return "CRITICAL"

        if risk > 5:

            return "HIGH"

        if risk > 3:

            return "MODERATE"

        return "LOW"