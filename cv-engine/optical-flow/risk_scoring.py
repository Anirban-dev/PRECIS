# cv_engine/optical_flow/risk_scoring.py

import logging
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("risk-scoring-engine")

# =========================================================
# CROWD RISK SCORING ENGINE
# =========================================================

class CrowdRiskScoringEngine:

    def __init__(self):

        logger.info(
            "Initializing Crowd Criticality Scoring Engine..."
        )

    # =====================================================
    # CALCULATE FINAL RISK SCORE
    # =====================================================

    def calculate_risk_score(
        self,
        person_count,
        turbulence_metrics,
        wave_metrics,
        audio_stress_level=0.0,
        screaming_detected=False
    ):

        """
        Combines:
        - YOLO crowd density
        - Optical flow turbulence
        - Crowd resonance
        - Acoustic stress telemetry
        """

        # -------------------------------------------------
        # EXTRACT METRICS
        # -------------------------------------------------

        turbulence_score = turbulence_metrics.get(
            "turbulence_score",
            0
        )

        instability_index = turbulence_metrics.get(
            "crowd_instability_index",
            0
        )

        passive_outstroke_probability = turbulence_metrics.get(
            "passive_outstroke_probability",
            0
        )

        resonance_score = wave_metrics.get(
            "resonance_score",
            0
        )

        shockwave_detected = wave_metrics.get(
            "shockwave_detected",
            False
        )

        directional_sync = wave_metrics.get(
            "directional_sync",
            0
        )

        # -------------------------------------------------
        # NORMALIZED DENSITY SCORE
        # -------------------------------------------------

        density_score = min(person_count / 100, 1.0)

        # -------------------------------------------------
        # AUDIO PANIC AMPLIFICATION
        # -------------------------------------------------

        audio_risk_boost = 0.0

        if audio_stress_level > 0.6:
            audio_risk_boost += 0.15

        if screaming_detected:
            audio_risk_boost += 0.25

        # -------------------------------------------------
        # SHOCKWAVE BOOST
        # -------------------------------------------------

        shockwave_boost = 0.0

        if shockwave_detected:
            shockwave_boost += 0.30

        # -------------------------------------------------
        # FINAL CROWD CRITICALITY INDEX
        # -------------------------------------------------

        crowd_criticality_index = (

            density_score * 0.20 +

            turbulence_score * 0.15 +

            instability_index * 0.20 +

            resonance_score * 0.20 +

            passive_outstroke_probability * 0.15 +

            directional_sync * 0.10 +

            audio_risk_boost +

            shockwave_boost
        )

        # -------------------------------------------------
        # NORMALIZE FINAL SCORE
        # -------------------------------------------------

        crowd_criticality_index = min(
            crowd_criticality_index,
            10.0
        )

        # -------------------------------------------------
        # RISK CLASSIFICATION
        # -------------------------------------------------

        if crowd_criticality_index < 2:

            risk_level = "LOW"

        elif crowd_criticality_index < 4:

            risk_level = "MODERATE"

        elif crowd_criticality_index < 6:

            risk_level = "HIGH"

        elif crowd_criticality_index < 8:

            risk_level = "SEVERE"

        else:

            risk_level = "CRITICAL"

        # -------------------------------------------------
        # EMERGENCY RESPONSE DECISION
        # -------------------------------------------------

        emergency_dispatch_required = False

        if risk_level in ["SEVERE", "CRITICAL"]:

            emergency_dispatch_required = True

        # -------------------------------------------------
        # PREVENTIVE ALERTS
        # -------------------------------------------------

        preventive_actions = []

        if risk_level == "HIGH":

            preventive_actions.extend([
                "Increase surveillance density",
                "Notify nearby security personnel",
                "Activate flow moderation protocols"
            ])

        elif risk_level == "SEVERE":

            preventive_actions.extend([
                "Dispatch rescue teams",
                "Alert nearest hospitals",
                "Notify crowd control police",
                "Activate emergency medical readiness"
            ])

        elif risk_level == "CRITICAL":

            preventive_actions.extend([
                "Trigger critical evacuation advisory",
                "Dispatch ambulance network",
                "Alert fire brigade",
                "Lock high-pressure entry zones",
                "Enable dynamic crowd steering"
            ])

        # -------------------------------------------------
        # FINAL REPORT
        # -------------------------------------------------

        report = {

            "timestamp": datetime.utcnow().isoformat(),

            "person_count": person_count,

            "crowd_criticality_index": round(
                crowd_criticality_index,
                4
            ),

            "risk_level": risk_level,

            "turbulence_score": round(
                turbulence_score,
                4
            ),

            "resonance_score": round(
                resonance_score,
                4
            ),

            "instability_index": round(
                instability_index,
                4
            ),

            "passive_outstroke_probability": round(
                passive_outstroke_probability,
                4
            ),

            "directional_sync": round(
                directional_sync,
                4
            ),

            "audio_stress_level": round(
                audio_stress_level,
                4
            ),

            "shockwave_detected": shockwave_detected,

            "screaming_detected": screaming_detected,

            "emergency_dispatch_required":
                emergency_dispatch_required,

            "preventive_actions":
                preventive_actions
        }

        # -------------------------------------------------
        # LOGGING
        # -------------------------------------------------

        logger.info(
            f"[RISK ENGINE] "
            f"CCI={crowd_criticality_index:.2f} | "
            f"Risk={risk_level} | "
            f"Emergency={emergency_dispatch_required}"
        )

        return report

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Crowd Risk Engine self-test..."
    )

    # -----------------------------------------------------
    # SYNTHETIC INPUTS
    # -----------------------------------------------------

    turbulence_metrics = {

        "turbulence_score": 6.4,

        "crowd_instability_index": 5.7,

        "passive_outstroke_probability": 0.72
    }

    wave_metrics = {

        "resonance_score": 7.8,

        "shockwave_detected": True,

        "directional_sync": 3.1
    }

    # -----------------------------------------------------
    # ENGINE INITIALIZATION
    # -----------------------------------------------------

    engine = CrowdRiskScoringEngine()

    # -----------------------------------------------------
    # RUN SCORING
    # -----------------------------------------------------

    result = engine.calculate_risk_score(

        person_count=85,

        turbulence_metrics=turbulence_metrics,

        wave_metrics=wave_metrics,

        audio_stress_level=0.82,

        screaming_detected=True
    )

    print("\n========== CROWD RISK REPORT ==========\n")

    for key, value in result.items():

        print(f"{key}: {value}")