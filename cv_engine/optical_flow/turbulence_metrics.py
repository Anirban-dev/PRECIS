# cv_engine/optical_flow/turbulence_metrics.py

import numpy as np
import logging
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("turbulence-engine")

# =========================================================
# TURBULENCE METRICS ENGINE
# =========================================================

class TurbulenceMetricsEngine:

    def __init__(self):

        logger.info("Initializing Crowd Turbulence Engine...")

    # =====================================================
    # CALCULATE TURBULENCE METRICS
    # =====================================================

    def calculate_metrics(self, flow):

        """
        flow:
            Optical flow matrix from Farneback algorithm
        """

        # -------------------------------------------------
        # FLOW COMPONENTS
        # -------------------------------------------------

        fx = flow[..., 0]
        fy = flow[..., 1]

        # -------------------------------------------------
        # MOTION MAGNITUDE
        # -------------------------------------------------

        magnitude = np.sqrt(fx**2 + fy**2)

        # -------------------------------------------------
        # BASIC MOTION STATISTICS
        # -------------------------------------------------

        mean_velocity = float(np.mean(magnitude))

        max_velocity = float(np.max(magnitude))

        velocity_variance = float(np.var(magnitude))

        motion_entropy = float(
            -np.sum(
                (magnitude / (np.sum(magnitude) + 1e-6))
                * np.log(
                    (magnitude / (np.sum(magnitude) + 1e-6))
                    + 1e-6
                )
            )
        )

        # -------------------------------------------------
        # DIRECTION ANALYSIS
        # -------------------------------------------------

        direction_angles = np.arctan2(fy, fx)

        directional_variance = float(
            np.var(direction_angles)
        )

        # -------------------------------------------------
        # TURBULENCE SCORE
        # -------------------------------------------------

        turbulence_score = float(
            (
                velocity_variance * 0.45
                +
                directional_variance * 0.35
                +
                motion_entropy * 0.20
            )
        )

        # -------------------------------------------------
        # RISK CLASSIFICATION
        # -------------------------------------------------

        if turbulence_score < 2.0:

            risk_level = "LOW"

        elif turbulence_score < 5.0:

            risk_level = "MEDIUM"

        elif turbulence_score < 8.0:

            risk_level = "HIGH"

        else:

            risk_level = "CRITICAL"

        # -------------------------------------------------
        # PASSIVE OUTSTROKE PROBABILITY
        # -------------------------------------------------

        passive_outstroke_probability = min(
            turbulence_score / 10,
            1.0
        )

        # -------------------------------------------------
        # CROWD INSTABILITY INDEX
        # -------------------------------------------------

        crowd_instability_index = float(
            (
                mean_velocity * 0.30
                +
                turbulence_score * 0.50
                +
                directional_variance * 0.20
            )
        )

        # -------------------------------------------------
        # FINAL METRICS
        # -------------------------------------------------

        metrics = {

            "timestamp": datetime.utcnow().isoformat(),

            "mean_velocity": round(mean_velocity, 4),

            "max_velocity": round(max_velocity, 4),

            "velocity_variance": round(velocity_variance, 4),

            "motion_entropy": round(motion_entropy, 4),

            "directional_variance": round(
                directional_variance,
                4
            ),

            "turbulence_score": round(
                turbulence_score,
                4
            ),

            "crowd_instability_index": round(
                crowd_instability_index,
                4
            ),

            "passive_outstroke_probability": round(
                passive_outstroke_probability,
                4
            ),

            "risk_level": risk_level
        }

        # -------------------------------------------------
        # LOGGING
        # -------------------------------------------------

        logger.info(
            f"[TURBULENCE] "
            f"Risk={risk_level} | "
            f"Score={turbulence_score:.2f} | "
            f"OutstrokeProb={passive_outstroke_probability:.2f}"
        )

        return metrics

# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    logger.info("Running turbulence engine self-test...")

    # -----------------------------------------------------
    # GENERATE DUMMY FLOW MATRIX
    # -----------------------------------------------------

    dummy_flow = np.random.randn(480, 640, 2)

    engine = TurbulenceMetricsEngine()

    result = engine.calculate_metrics(dummy_flow)

    print("\n========== TURBULENCE REPORT ==========\n")

    for key, value in result.items():

        print(f"{key}: {value}")