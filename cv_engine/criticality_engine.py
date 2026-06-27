from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "criticality-engine"
)


class CriticalityEngine:

    def __init__(self):

        logger.info(
            "Initializing Criticality Engine..."
        )

    def evaluate_criticality(

        self,

        fusion_score,

        turbulence_score,

        bottleneck_score,

        evacuation_complexity,

        outstroke_probability
    ):

        logger.info(
            "Calculating unified crowd criticality..."
        )

        criticality_score = (

            fusion_score * 0.25 +

            turbulence_score * 0.20 +

            bottleneck_score * 0.20 +

            evacuation_complexity * 0.20 +

            outstroke_probability * 10 * 0.15
        )

        criticality_score = min(
            criticality_score,
            10.0
        )

        risk_level = "LOW"

        if criticality_score > 8:

            risk_level = "CRITICAL"

        elif criticality_score > 6:

            risk_level = "SEVERE"

        elif criticality_score > 4:

            risk_level = "HIGH"

        elif criticality_score > 2:

            risk_level = "MODERATE"

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "criticality_score":
                round(criticality_score, 2),

            "risk_level":
                risk_level
        }

        logger.info(

            f"[CRITICALITY] "

            f"Risk={risk_level} | "

            f"Score={criticality_score:.2f}"
        )

        return report