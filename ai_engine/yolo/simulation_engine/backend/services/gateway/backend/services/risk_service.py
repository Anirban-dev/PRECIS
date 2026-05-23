from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "risk-service"
)


class RiskService:

    def __init__(self):

        logger.info(
            "Initializing Risk Evaluation Service..."
        )

    def evaluate_risk(

        self,

        analytics
    ):

        logger.info(
            "Evaluating crowd danger levels..."
        )

        density = analytics.get(
            "crowd_density",
            0.0
        )

        turbulence = analytics.get(
            "turbulence_score",
            0.0
        )

        resonance = analytics.get(
            "resonance_probability",
            0.0
        )

        risk_score = (

            density * 0.30 +

            turbulence * 0.40 +

            resonance * 10 * 0.30
        )

        risk_score = min(
            risk_score,
            10.0
        )

        risk_level = "LOW"

        if risk_score > 8:

            risk_level = "CRITICAL"

        elif risk_score > 6:

            risk_level = "SEVERE"

        elif risk_score > 4:

            risk_level = "HIGH"

        elif risk_score > 2:

            risk_level = "MODERATE"

        emergency_required = False

        if risk_level in [
            "SEVERE",
            "CRITICAL"
        ]:

            emergency_required = True

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "risk_score":
                round(risk_score, 2),

            "risk_level":
                risk_level,

            "emergency_required":
                emergency_required
        }

        logger.info(

            f"[RISK] "

            f"Level={risk_level} | "

            f"Score={risk_score:.2f}"
        )

        return report


if __name__ == "__main__":

    analytics = {

        "crowd_density": 8.2,

        "turbulence_score": 7.4,

        "resonance_probability": 0.81
    }

    service = RiskService()

    result = service.evaluate_risk(
        analytics
    )

    print(result)