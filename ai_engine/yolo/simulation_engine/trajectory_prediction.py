import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "trajectory-prediction-engine"
)


class TrajectoryPredictionEngine:

    def __init__(self):

        logger.info(
            "Initializing Trajectory Prediction Engine..."
        )

    def predict_trajectory(

        self,

        motion_vectors,

        turbulence_metrics,

        resonance_metrics,

        prediction_horizon=30
    ):

        logger.info(
            "Running crowd trajectory prediction..."
        )

        if len(motion_vectors) == 0:

            raise Exception(
                "No motion vectors available."
            )

        vectors = np.array(motion_vectors)

        x_velocity = vectors[:, 0]

        y_velocity = vectors[:, 1]

        mean_x_velocity = float(
            np.mean(x_velocity)
        )

        mean_y_velocity = float(
            np.mean(y_velocity)
        )

        velocity_magnitude = float(

            np.sqrt(

                mean_x_velocity ** 2 +

                mean_y_velocity ** 2
            )
        )

        directional_variance = float(

            np.var(x_velocity) +

            np.var(y_velocity)
        )

        turbulence_score = (
            turbulence_metrics.get(
                "turbulence_score",
                0.0
            )
        )

        resonance_probability = (
            resonance_metrics.get(
                "resonance_probability",
                0.0
            )
        )

        future_positions = []

        current_x = 0.0

        current_y = 0.0

        instability_factor = (

            turbulence_score * 0.08 +

            resonance_probability * 0.4
        )

        for step in range(prediction_horizon):

            drift_x = np.random.normal(
                0,
                instability_factor
            )

            drift_y = np.random.normal(
                0,
                instability_factor
            )

            current_x += (
                mean_x_velocity + drift_x
            )

            current_y += (
                mean_y_velocity + drift_y
            )

            future_positions.append({

                "time_step": step + 1,

                "predicted_x":
                    round(current_x, 4),

                "predicted_y":
                    round(current_y, 4)
            })

        directional_state = "STABLE"

        if directional_variance > 4:

            directional_state = "CHAOTIC"

        elif directional_variance > 2:

            directional_state = "UNSTABLE"

        trajectory_risk = "LOW"

        if (
            turbulence_score > 6
            and resonance_probability > 0.7
        ):

            trajectory_risk = "CRITICAL"

        elif turbulence_score > 4:

            trajectory_risk = "HIGH"

        elif turbulence_score > 2:

            trajectory_risk = "MODERATE"

        predicted_flow_direction = {

            "x_direction":
                round(mean_x_velocity, 4),

            "y_direction":
                round(mean_y_velocity, 4)
        }

        trajectory_stability_score = max(

            0.0,

            10 - (
                directional_variance +
                turbulence_score
            )
        )

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "prediction_horizon":
                prediction_horizon,

            "velocity_magnitude":
                round(
                    velocity_magnitude,
                    4
                ),

            "directional_variance":
                round(
                    directional_variance,
                    4
                ),

            "directional_state":
                directional_state,

            "trajectory_risk":
                trajectory_risk,

            "trajectory_stability_score":
                round(
                    trajectory_stability_score,
                    4
                ),

            "predicted_flow_direction":
                predicted_flow_direction,

            "future_positions":
                future_positions
        }

        logger.info(

            f"[TRAJECTORY ENGINE] "

            f"Risk={trajectory_risk} | "

            f"DirectionalState={directional_state}"
        )

        return report


if __name__ == "__main__":

    motion_vectors = [

        [1.2, 0.8],

        [1.5, 1.1],

        [0.9, 0.6],

        [1.7, 1.4],

        [1.3, 0.7]
    ]

    turbulence_metrics = {

        "turbulence_score": 5.8
    }

    resonance_metrics = {

        "resonance_probability": 0.81
    }

    try:

        engine = TrajectoryPredictionEngine()

        result = engine.predict_trajectory(

            motion_vectors,

            turbulence_metrics,

            resonance_metrics,

            prediction_horizon=20
        )

        print(
            "\n========== TRAJECTORY REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Trajectory Prediction Error: {e}"
        )