import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "bottleneck-prediction-engine"
)


class BottleneckPredictionEngine:

    def __init__(self):

        logger.info(
            "Initializing Bottleneck Prediction Engine..."
        )

    def predict_bottleneck(

        self,

        motion_metrics,

        turbulence_metrics,

        resonance_metrics,

        crowd_density_map
    ):

        logger.info(
            "Running bottleneck prediction analysis..."
        )

        mean_velocity = motion_metrics.get(
            "mean_velocity",
            0.0
        )

        motion_coherence = motion_metrics.get(
            "motion_coherence",
            0.0
        )

        turbulence_score = (
            turbulence_metrics.get(
                "turbulence_score",
                0.0
            )
        )

        instability_index = (
            turbulence_metrics.get(
                "crowd_instability_index",
                0.0
            )
        )

        resonance_score = (
            resonance_metrics.get(
                "resonance_score",
                0.0
            )
        )

        resonance_probability = (
            resonance_metrics.get(
                "resonance_probability",
                0.0
            )
        )

        max_density = float(
            np.max(crowd_density_map)
        )

        average_density = float(
            np.mean(crowd_density_map)
        )

        density_variation = float(
            np.std(crowd_density_map)
        )

        bottleneck_score = (

            max_density * 0.25 +

            average_density * 0.15 +

            density_variation * 0.15 +

            turbulence_score * 0.15 +

            instability_index * 0.10 +

            resonance_score * 0.10 +

            resonance_probability * 5 +

            motion_coherence * 2 -

            mean_velocity * 0.05
        )

        bottleneck_score = min(
            bottleneck_score,
            10.0
        )

        if bottleneck_score < 2:

            bottleneck_risk = "LOW"

        elif bottleneck_score < 4:

            bottleneck_risk = "MODERATE"

        elif bottleneck_score < 7:

            bottleneck_risk = "HIGH"

        else:

            bottleneck_risk = "CRITICAL"

        pressure_zone_detected = False

        if (
            max_density > 7
            and turbulence_score > 5
        ):

            pressure_zone_detected = True

        collapse_probability = round(
            bottleneck_score / 10,
            4
        )

        predicted_time_to_failure = None

        if bottleneck_risk == "CRITICAL":

            predicted_time_to_failure = (
                "30-90 seconds"
            )

        elif bottleneck_risk == "HIGH":

            predicted_time_to_failure = (
                "2-5 minutes"
            )

        elif bottleneck_risk == "MODERATE":

            predicted_time_to_failure = (
                "5-12 minutes"
            )

        hotspot_index = np.unravel_index(
            np.argmax(crowd_density_map),
            crowd_density_map.shape
        )

        preventive_actions = []

        if bottleneck_risk == "HIGH":

            preventive_actions.extend([

                "Reduce incoming crowd flow",

                "Deploy crowd control personnel",

                "Activate directional guidance",

                "Monitor pressure escalation"
            ])

        elif bottleneck_risk == "CRITICAL":

            preventive_actions.extend([

                "Trigger emergency crowd diversion",

                "Alert emergency medical teams",

                "Notify police control room",

                "Prepare evacuation routes",

                "Alert nearby hospitals"
            ])

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "bottleneck_score":
                round(
                    bottleneck_score,
                    4
                ),

            "bottleneck_risk":
                bottleneck_risk,

            "collapse_probability":
                collapse_probability,

            "pressure_zone_detected":
                pressure_zone_detected,

            "predicted_time_to_failure":
                predicted_time_to_failure,

            "hotspot_coordinates": {

                "x": int(hotspot_index[1]),

                "y": int(hotspot_index[0])
            },

            "max_density":
                round(max_density, 4),

            "average_density":
                round(average_density, 4),

            "density_variation":
                round(density_variation, 4),

            "preventive_actions":
                preventive_actions
        }

        logger.info(

            f"[BOTTLENECK ENGINE] "

            f"Risk={bottleneck_risk} | "

            f"Score={bottleneck_score:.2f} | "

            f"CollapseProbability={collapse_probability:.2f}"
        )

        return report


if __name__ == "__main__":

    motion_metrics = {

        "mean_velocity": 3.8,

        "motion_coherence": 0.84
    }

    turbulence_metrics = {

        "turbulence_score": 6.9,

        "crowd_instability_index": 5.8
    }

    resonance_metrics = {

        "resonance_score": 7.6,

        "resonance_probability": 0.88
    }

    crowd_density_map = np.random.uniform(
        1,
        9,
        (20, 20)
    )

    try:

        engine = BottleneckPredictionEngine()

        result = engine.predict_bottleneck(

            motion_metrics,

            turbulence_metrics,

            resonance_metrics,

            crowd_density_map
        )

        print(
            "\n========== BOTTLENECK REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Bottleneck Prediction Error: {e}"
        )