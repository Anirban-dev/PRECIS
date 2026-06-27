# cv_engine/fusion_engine.py

import logging
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("fusion-engine")

# =========================================================
# MULTI-MODAL FUSION ENGINE
# =========================================================

class FusionEngine:

    def __init__(self):

        logger.info(
            "Initializing Multi-Modal Fusion Engine..."
        )

    # =====================================================
    # FUSE ALL ANALYTICS
    # =====================================================

    def fuse_intelligence(

        self,

        yolo_metrics,

        motion_metrics,

        turbulence_metrics,

        wave_metrics,

        resonance_metrics,

        audio_metrics=None
    ):

        """
        Combines:
        - YOLO crowd analytics
        - Motion vectors
        - Turbulence metrics
        - Crowd wave detection
        - Resonance scoring
        - Acoustic stress telemetry
        """

        logger.info(
            "Starting intelligence fusion process..."
        )

        # -------------------------------------------------
        # YOLO METRICS
        # -------------------------------------------------

        person_count = yolo_metrics.get(
            "person_count",
            0
        )

        density_score = yolo_metrics.get(
            "density_score",
            0.0
        )

        # -------------------------------------------------
        # MOTION METRICS
        # -------------------------------------------------

        mean_velocity = motion_metrics.get(
            "mean_velocity",
            0.0
        )

        dominant_direction = motion_metrics.get(
            "dominant_direction",
            0.0
        )

        motion_coherence = motion_metrics.get(
            "motion_coherence",
            0.0
        )

        # -------------------------------------------------
        # TURBULENCE METRICS
        # -------------------------------------------------

        turbulence_score = turbulence_metrics.get(
            "turbulence_score",
            0.0
        )

        instability_index = turbulence_metrics.get(
            "crowd_instability_index",
            0.0
        )

        passive_outstroke_probability = (
            turbulence_metrics.get(
                "passive_outstroke_probability",
                0.0
            )
        )

        # -------------------------------------------------
        # WAVE METRICS
        # -------------------------------------------------

        resonance_level = wave_metrics.get(
            "resonance_level",
            "STABLE"
        )

        shockwave_detected = wave_metrics.get(
            "shockwave_detected",
            False
        )

        oscillation_strength = wave_metrics.get(
            "oscillation_strength",
            0.0
        )

        # -------------------------------------------------
        # RESONANCE METRICS
        # -------------------------------------------------

        resonance_score = resonance_metrics.get(
            "resonance_score",
            0.0
        )

        resonance_probability = (
            resonance_metrics.get(
                "resonance_probability",
                0.0
            )
        )

        # -------------------------------------------------
        # AUDIO METRICS
        # -------------------------------------------------

        audio_stress_level = 0.0

        screaming_detected = False

        decibel_level = 0.0

        if audio_metrics:

            audio_stress_level = (
                audio_metrics.get(
                    "stress_pitch_drift",
                    0.0
                )
            )

            screaming_detected = (
                audio_metrics.get(
                    "screaming_detected",
                    False
                )
            )

            decibel_level = (
                audio_metrics.get(
                    "decibel_level",
                    0.0
                )
            )

        # -------------------------------------------------
        # MULTI-MODAL FUSION SCORE
        # -------------------------------------------------

        fusion_score = (

            density_score * 0.10 +

            mean_velocity * 0.10 +

            motion_coherence * 0.10 +

            turbulence_score * 0.15 +

            instability_index * 0.15 +

            oscillation_strength * 0.10 +

            resonance_score * 0.15 +

            resonance_probability * 0.10 +

            audio_stress_level * 0.05
        )

        # -------------------------------------------------
        # SHOCKWAVE AMPLIFICATION
        # -------------------------------------------------

        if shockwave_detected:

            fusion_score += 1.0

        # -------------------------------------------------
        # SCREAMING AMPLIFICATION
        # -------------------------------------------------

        if screaming_detected:

            fusion_score += 0.5

        # -------------------------------------------------
        # NORMALIZATION
        # -------------------------------------------------

        fusion_score = min(fusion_score, 10.0)

        # -------------------------------------------------
        # FUSION RISK CLASSIFICATION
        # -------------------------------------------------

        if fusion_score < 2:

            fusion_risk = "LOW"

        elif fusion_score < 4:

            fusion_risk = "MODERATE"

        elif fusion_score < 6:

            fusion_risk = "HIGH"

        elif fusion_score < 8:

            fusion_risk = "SEVERE"

        else:

            fusion_risk = "CRITICAL"

        # -------------------------------------------------
        # PRE-DISASTER STATE DETECTION
        # -------------------------------------------------

        pre_disaster_state = False

        if (
            turbulence_score > 5
            and resonance_probability > 0.6
            and oscillation_strength > 1.5
        ):

            pre_disaster_state = True

        # -------------------------------------------------
        # CROWD STATE
        # -------------------------------------------------

        crowd_state = "NORMAL"

        if fusion_risk == "HIGH":

            crowd_state = "UNSTABLE"

        elif fusion_risk == "SEVERE":

            crowd_state = "DANGEROUS"

        elif fusion_risk == "CRITICAL":

            crowd_state = "COLLAPSE_IMMINENT"

        # -------------------------------------------------
        # FINAL FUSION REPORT
        # -------------------------------------------------

        fusion_report = {

            "timestamp": datetime.utcnow().isoformat(),

            "person_count": person_count,

            "density_score": round(
                density_score,
                4
            ),

            "mean_velocity": round(
                mean_velocity,
                4
            ),

            "dominant_direction": round(
                dominant_direction,
                4
            ),

            "motion_coherence": round(
                motion_coherence,
                4
            ),

            "turbulence_score": round(
                turbulence_score,
                4
            ),

            "instability_index": round(
                instability_index,
                4
            ),

            "oscillation_strength": round(
                oscillation_strength,
                4
            ),

            "resonance_score": round(
                resonance_score,
                4
            ),

            "resonance_probability": round(
                resonance_probability,
                4
            ),

            "audio_stress_level": round(
                audio_stress_level,
                4
            ),

            "decibel_level": round(
                decibel_level,
                2
            ),

            "shockwave_detected":
                shockwave_detected,

            "screaming_detected":
                screaming_detected,

            "passive_outstroke_probability":
                round(
                    passive_outstroke_probability,
                    4
                ),

            "fusion_score":
                round(fusion_score, 4),

            "fusion_risk":
                fusion_risk,

            "crowd_state":
                crowd_state,

            "pre_disaster_state":
                pre_disaster_state
        }

        # -------------------------------------------------
        # LOGGING
        # -------------------------------------------------

        logger.info(

            f"[FUSION ENGINE] "

            f"FusionRisk={fusion_risk} | "

            f"FusionScore={fusion_score:.2f} | "

            f"PreDisaster={pre_disaster_state}"
        )

        return fusion_report

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Fusion Engine self-test..."
    )

    # -----------------------------------------------------
    # SYNTHETIC INPUTS
    # -----------------------------------------------------

    yolo_metrics = {

        "person_count": 120,

        "density_score": 7.2
    }

    motion_metrics = {

        "mean_velocity": 3.8,

        "dominant_direction": 82,

        "motion_coherence": 0.76
    }

    turbulence_metrics = {

        "turbulence_score": 6.4,

        "crowd_instability_index": 5.9,

        "passive_outstroke_probability": 0.74
    }

    wave_metrics = {

        "resonance_level": "UNSTABLE",

        "shockwave_detected": True,

        "oscillation_strength": 2.1
    }

    resonance_metrics = {

        "resonance_score": 7.4,

        "resonance_probability": 0.82
    }

    audio_metrics = {

        "stress_pitch_drift": 0.78,

        "screaming_detected": True,

        "decibel_level": 92.5
    }

    # -----------------------------------------------------
    # RUN ENGINE
    # -----------------------------------------------------

    engine = FusionEngine()

    result = engine.fuse_intelligence(

        yolo_metrics,

        motion_metrics,

        turbulence_metrics,

        wave_metrics,

        resonance_metrics,

        audio_metrics
    )

    print(
        "\n========== FUSION REPORT ==========\n"
    )

    for key, value in result.items():

        print(f"{key}: {value}")