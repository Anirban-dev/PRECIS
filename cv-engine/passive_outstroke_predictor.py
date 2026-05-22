# cv_engine/passive_outstroke_predictor.py

import logging
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "passive-outstroke-predictor"
)

# =========================================================
# PASSIVE OUTSTROKE PREDICTOR
# =========================================================

class PassiveOutstrokePredictor:

    def __init__(self):

        logger.info(
            "Initializing Passive Outstroke Predictor..."
        )

    # =====================================================
    # PREDICT OUTSTROKE EVENT
    # =====================================================

    def predict_outstroke(

        self,

        turbulence_metrics,

        wave_metrics,

        resonance_metrics,

        fusion_metrics
    ):

        """
        Predicts probability of:

        - uncontrolled crowd surges
        - pressure collapse
        - synchronized push events
        - shockwave propagation
        """

        logger.info(
            "Running passive outstroke analysis..."
        )

        # -------------------------------------------------
        # TURBULENCE DATA
        # -------------------------------------------------

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

        # -------------------------------------------------
        # WAVE DATA
        # -------------------------------------------------

        oscillation_strength = (
            wave_metrics.get(
                "oscillation_strength",
                0.0
            )
        )

        directional_sync = (
            wave_metrics.get(
                "directional_sync",
                0.0
            )
        )

        shockwave_detected = (
            wave_metrics.get(
                "shockwave_detected",
                False
            )
        )

        # -------------------------------------------------
        # RESONANCE DATA
        # -------------------------------------------------

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

        # -------------------------------------------------
        # FUSION DATA
        # -------------------------------------------------

        fusion_score = (
            fusion_metrics.get(
                "fusion_score",
                0.0
            )
        )

        crowd_state = (
            fusion_metrics.get(
                "crowd_state",
                "NORMAL"
            )
        )

        # -------------------------------------------------
        # BASE OUTSTROKE SCORE
        # -------------------------------------------------

        outstroke_score = (

            turbulence_score * 0.20 +

            instability_index * 0.20 +

            oscillation_strength * 0.15 +

            directional_sync * 0.10 +

            resonance_score * 0.20 +

            resonance_probability * 0.10 +

            fusion_score * 0.05
        )

        # -------------------------------------------------
        # SHOCKWAVE AMPLIFICATION
        # -------------------------------------------------

        if shockwave_detected:

            outstroke_score += 1.2

        # -------------------------------------------------
        # CROWD COLLAPSE AMPLIFICATION
        # -------------------------------------------------

        if crowd_state == "COLLAPSE_IMMINENT":

            outstroke_score += 1.5

        elif crowd_state == "DANGEROUS":

            outstroke_score += 0.8

        # -------------------------------------------------
        # NORMALIZATION
        # -------------------------------------------------

        outstroke_score = min(
            outstroke_score,
            10.0
        )

        # -------------------------------------------------
        # OUTSTROKE PROBABILITY
        # -------------------------------------------------

        outstroke_probability = round(
            outstroke_score / 10,
            4
        )

        # -------------------------------------------------
        # RISK CLASSIFICATION
        # -------------------------------------------------

        if outstroke_probability < 0.25:

            outstroke_risk = "LOW"

        elif outstroke_probability < 0.50:

            outstroke_risk = "MODERATE"

        elif outstroke_probability < 0.75:

            outstroke_risk = "HIGH"

        else:

            outstroke_risk = "CRITICAL"

        # -------------------------------------------------
        # EARLY WARNING DETECTION
        # -------------------------------------------------

        early_warning = False

        if (

            turbulence_score > 5

            and resonance_probability > 0.60

            and oscillation_strength > 1.5
        ):

            early_warning = True

        # -------------------------------------------------
        # COLLAPSE TIME ESTIMATION
        # -------------------------------------------------

        estimated_collapse_window = None

        if outstroke_risk == "CRITICAL":

            estimated_collapse_window = (
                "30-90 seconds"
            )

        elif outstroke_risk == "HIGH":

            estimated_collapse_window = (
                "2-5 minutes"
            )

        elif outstroke_risk == "MODERATE":

            estimated_collapse_window = (
                "5-10 minutes"
            )

        # -------------------------------------------------
        # PREVENTIVE ACTIONS
        # -------------------------------------------------

        preventive_actions = []

        if outstroke_risk == "HIGH":

            preventive_actions.extend([

                "Increase surveillance density",

                "Notify crowd-control teams",

                "Reduce inflow pressure",

                "Enable directional crowd guidance"
            ])

        elif outstroke_risk == "CRITICAL":

            preventive_actions.extend([

                "Dispatch emergency rescue units",

                "Alert nearby hospitals",

                "Notify ambulance network",

                "Alert police command center",

                "Prepare emergency evacuation",

                "Activate crowd steering system"
            ])

        # -------------------------------------------------
        # FINAL REPORT
        # -------------------------------------------------

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "outstroke_score":
                round(outstroke_score, 4),

            "outstroke_probability":
                outstroke_probability,

            "outstroke_risk":
                outstroke_risk,

            "early_warning":
                early_warning,

            "shockwave_detected":
                shockwave_detected,

            "crowd_state":
                crowd_state,

            "estimated_collapse_window":
                estimated_collapse_window,

            "preventive_actions":
                preventive_actions
        }

        # -------------------------------------------------
        # LOGGING
        # -------------------------------------------------

        logger.info(

            f"[OUTSTROKE PREDICTOR] "

            f"Risk={outstroke_risk} | "

            f"Probability={outstroke_probability:.2f} | "

            f"EarlyWarning={early_warning}"
        )

        return report

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Passive Outstroke Predictor test..."
    )

    # -----------------------------------------------------
    # SYNTHETIC TEST DATA
    # -----------------------------------------------------

    turbulence_metrics = {

        "turbulence_score": 6.8,

        "crowd_instability_index": 6.2
    }

    wave_metrics = {

        "oscillation_strength": 2.4,

        "directional_sync": 3.5,

        "shockwave_detected": True
    }

    resonance_metrics = {

        "resonance_score": 7.9,

        "resonance_probability": 0.84
    }

    fusion_metrics = {

        "fusion_score": 8.3,

        "crowd_state": "COLLAPSE_IMMINENT"
    }

    # -----------------------------------------------------
    # RUN PREDICTOR
    # -----------------------------------------------------

    predictor = PassiveOutstrokePredictor()

    result = predictor.predict_outstroke(

        turbulence_metrics,

        wave_metrics,

        resonance_metrics,

        fusion_metrics
    )

    print(
        "\n========== OUTSTROKE REPORT ==========\n"
    )

    for key, value in result.items():

        print(f"{key}: {value}")