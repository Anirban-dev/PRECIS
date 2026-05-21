# cv_engine/optical_flow/crowd_wave_detector.py

import numpy as np
import logging
from collections import deque
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("crowd-wave-detector")

# =========================================================
# CROWD WAVE DETECTOR ENGINE
# =========================================================

class CrowdWaveDetector:

    def __init__(self, history_size=30):

        logger.info(
            "Initializing Crowd Resonance & Wave Detector..."
        )

        # ---------------------------------------------
        # STORE TEMPORAL HISTORY
        # ---------------------------------------------

        self.magnitude_history = deque(maxlen=history_size)

        self.direction_history = deque(maxlen=history_size)

    # =====================================================
    # ANALYZE FLOW FIELD
    # =====================================================

    def analyze_wave_patterns(self, flow):

        """
        Detects synchronized crowd oscillation patterns
        from optical flow fields.
        """

        # -------------------------------------------------
        # FLOW COMPONENTS
        # -------------------------------------------------

        fx = flow[..., 0]
        fy = flow[..., 1]

        # -------------------------------------------------
        # MAGNITUDE + DIRECTION
        # -------------------------------------------------

        magnitude = np.sqrt(fx**2 + fy**2)

        direction = np.arctan2(fy, fx)

        mean_magnitude = float(np.mean(magnitude))

        mean_direction = float(np.mean(direction))

        # -------------------------------------------------
        # STORE TEMPORAL HISTORY
        # -------------------------------------------------

        self.magnitude_history.append(mean_magnitude)

        self.direction_history.append(mean_direction)

        # -------------------------------------------------
        # TEMPORAL ANALYSIS
        # -------------------------------------------------

        magnitude_array = np.array(
            self.magnitude_history
        )

        direction_array = np.array(
            self.direction_history
        )

        # -------------------------------------------------
        # OSCILLATION ANALYSIS
        # -------------------------------------------------

        oscillation_strength = float(
            np.std(magnitude_array)
        )

        directional_sync = float(
            1 / (
                np.var(direction_array) + 1e-6
            )
        )

        # -------------------------------------------------
        # FOURIER ANALYSIS
        # -------------------------------------------------

        if len(magnitude_array) > 5:

            fft_result = np.fft.fft(magnitude_array)

            frequencies = np.abs(fft_result)

            dominant_frequency = float(
                np.argmax(frequencies[1:]) + 1
            )

        else:

            dominant_frequency = 0.0

        # -------------------------------------------------
        # RESONANCE SCORE
        # -------------------------------------------------

        resonance_score = float(
            (
                oscillation_strength * 0.4
                +
                directional_sync * 0.4
                +
                dominant_frequency * 0.2
            )
        )

        # -------------------------------------------------
        # WAVE CLASSIFICATION
        # -------------------------------------------------

        if resonance_score < 2:

            resonance_level = "STABLE"

        elif resonance_score < 5:

            resonance_level = "OSCILLATING"

        elif resonance_score < 8:

            resonance_level = "UNSTABLE"

        else:

            resonance_level = "CRITICAL_RESONANCE"

        # -------------------------------------------------
        # PASSIVE OUTSTROKE PROBABILITY
        # -------------------------------------------------

        passive_outstroke_probability = min(
            resonance_score / 10,
            1.0
        )

        # -------------------------------------------------
        # SHOCKWAVE DETECTION
        # -------------------------------------------------

        shockwave_detected = False

        if (
            resonance_level == "CRITICAL_RESONANCE"
            and dominant_frequency > 3
        ):

            shockwave_detected = True

        # -------------------------------------------------
        # FINAL ANALYSIS
        # -------------------------------------------------

        analysis = {

            "timestamp": datetime.utcnow().isoformat(),

            "mean_motion_magnitude": round(
                mean_magnitude,
                4
            ),

            "oscillation_strength": round(
                oscillation_strength,
                4
            ),

            "directional_sync": round(
                directional_sync,
                4
            ),

            "dominant_frequency": round(
                dominant_frequency,
                4
            ),

            "resonance_score": round(
                resonance_score,
                4
            ),

            "resonance_level": resonance_level,

            "passive_outstroke_probability": round(
                passive_outstroke_probability,
                4
            ),

            "shockwave_detected": shockwave_detected
        }

        # -------------------------------------------------
        # LOGGING
        # -------------------------------------------------

        logger.info(
            f"[WAVE DETECTOR] "
            f"Level={resonance_level} | "
            f"Resonance={resonance_score:.2f} | "
            f"Shockwave={shockwave_detected}"
        )

        return analysis

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info("Running Crowd Wave Detector self-test...")

    # -----------------------------------------------------
    # GENERATE SYNTHETIC FLOW FIELD
    # -----------------------------------------------------

    synthetic_flow = np.random.randn(
        480,
        640,
        2
    )

    detector = CrowdWaveDetector()

    result = detector.analyze_wave_patterns(
        synthetic_flow
    )

    print("\n========== CROWD WAVE REPORT ==========\n")

    for key, value in result.items():

        print(f"{key}: {value}")