from datetime import datetime
import logging
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "analytics-service"
)


class AnalyticsService:

    def __init__(self):

        logger.info(
            "Initializing Crowd Analytics Service..."
        )

    def generate_live_analytics(self):

        logger.info(
            "Generating live crowd analytics..."
        )

        crowd_density = round(
            random.uniform(1.0, 9.5),
            2
        )

        turbulence_score = round(
            random.uniform(0.5, 8.8),
            2
        )

        resonance_probability = round(
            random.uniform(0.05, 0.95),
            2
        )

        shockwave_detected = False

        if (
            turbulence_score > 6
            and resonance_probability > 0.7
        ):

            shockwave_detected = True

        crowd_state = "STABLE"

        if turbulence_score > 7:

            crowd_state = "CRITICAL"

        elif turbulence_score > 5:

            crowd_state = "UNSTABLE"

        elif turbulence_score > 3:

            crowd_state = "ELEVATED"

        analytics = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "crowd_density":
                crowd_density,

            "turbulence_score":
                turbulence_score,

            "resonance_probability":
                resonance_probability,

            "shockwave_detected":
                shockwave_detected,

            "crowd_state":
                crowd_state
        }

        logger.info(

            f"[ANALYTICS] "

            f"Density={crowd_density} | "

            f"Turbulence={turbulence_score}"
        )

        return analytics


if __name__ == "__main__":

    service = AnalyticsService()

    result = service.generate_live_analytics()

    print(result)