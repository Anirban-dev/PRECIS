# cv_engine/dashboard_payload_builder.py

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
    "dashboard-payload-builder"
)

# =========================================================
# DASHBOARD PAYLOAD BUILDER
# =========================================================

class DashboardPayloadBuilder:

    def __init__(self):

        logger.info(
            "Initializing Dashboard Payload Builder..."
        )

    # =====================================================
    # BUILD DASHBOARD PAYLOAD
    # =====================================================

    def build_payload(

        self,

        fusion_report,

        risk_report,

        outstroke_report,

        resonance_metrics,

        turbulence_metrics,

        motion_metrics
    ):

        """
        Converts backend intelligence
        into frontend/dashboard-ready payloads.
        """

        logger.info(
            "Building dashboard payload..."
        )

        # -------------------------------------------------
        # BASIC STATUS
        # -------------------------------------------------

        crowd_state = fusion_report.get(
            "crowd_state",
            "UNKNOWN"
        )

        fusion_risk = fusion_report.get(
            "fusion_risk",
            "LOW"
        )

        fusion_score = fusion_report.get(
            "fusion_score",
            0.0
        )

        # -------------------------------------------------
        # RISK DATA
        # -------------------------------------------------

        crowd_criticality_index = (
            risk_report.get(
                "crowd_criticality_index",
                0.0
            )
        )

        risk_level = risk_report.get(
            "risk_level",
            "LOW"
        )

        emergency_dispatch_required = (
            risk_report.get(
                "emergency_dispatch_required",
                False
            )
        )

        # -------------------------------------------------
        # OUTSTROKE DATA
        # -------------------------------------------------

        outstroke_probability = (
            outstroke_report.get(
                "outstroke_probability",
                0.0
            )
        )

        outstroke_risk = (
            outstroke_report.get(
                "outstroke_risk",
                "LOW"
            )
        )

        early_warning = (
            outstroke_report.get(
                "early_warning",
                False
            )
        )

        collapse_window = (
            outstroke_report.get(
                "estimated_collapse_window",
                None
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
        # MOTION DATA
        # -------------------------------------------------

        mean_velocity = motion_metrics.get(
            "mean_velocity",
            0.0
        )

        dominant_direction = motion_metrics.get(
            "dominant_direction",
            0.0
        )

        # -------------------------------------------------
        # ALERT STATUS
        # -------------------------------------------------

        alert_status = "NORMAL"

        if risk_level == "HIGH":

            alert_status = "WARNING"

        elif risk_level == "SEVERE":

            alert_status = "EMERGENCY"

        elif risk_level == "CRITICAL":

            alert_status = "CRITICAL_ALERT"

        # -------------------------------------------------
        # FRONTEND COLOR STATE
        # -------------------------------------------------

        ui_color = "green"

        if alert_status == "WARNING":

            ui_color = "yellow"

        elif alert_status == "EMERGENCY":

            ui_color = "orange"

        elif alert_status == "CRITICAL_ALERT":

            ui_color = "red"

        # -------------------------------------------------
        # SYSTEM RECOMMENDATION
        # -------------------------------------------------

        recommendation = "Crowd Stable"

        if early_warning:

            recommendation = (
                "Preventive Intervention Recommended"
            )

        if emergency_dispatch_required:

            recommendation = (
                "Immediate Emergency Deployment Required"
            )

        # -------------------------------------------------
        # BUILD FINAL PAYLOAD
        # -------------------------------------------------

        payload = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "dashboard_status": {

                "crowd_state":
                    crowd_state,

                "alert_status":
                    alert_status,

                "ui_color":
                    ui_color,

                "recommendation":
                    recommendation
            },

            "crowd_metrics": {

                "fusion_score":
                    round(fusion_score, 4),

                "crowd_criticality_index":
                    round(
                        crowd_criticality_index,
                        4
                    ),

                "risk_level":
                    risk_level,

                "outstroke_probability":
                    round(
                        outstroke_probability,
                        4
                    ),

                "outstroke_risk":
                    outstroke_risk
            },

            "motion_analytics": {

                "mean_velocity":
                    round(mean_velocity, 4),

                "dominant_direction":
                    round(
                        dominant_direction,
                        4
                    ),

                "turbulence_score":
                    round(
                        turbulence_score,
                        4
                    ),

                "instability_index":
                    round(
                        instability_index,
                        4
                    )
            },

            "resonance_analytics": {

                "resonance_score":
                    round(
                        resonance_score,
                        4
                    ),

                "resonance_probability":
                    round(
                        resonance_probability,
                        4
                    )
            },

            "prediction_engine": {

                "early_warning":
                    early_warning,

                "estimated_collapse_window":
                    collapse_window,

                "emergency_dispatch_required":
                    emergency_dispatch_required
            }
        }

        logger.info(

            f"[DASHBOARD PAYLOAD] "

            f"Alert={alert_status} | "

            f"Risk={risk_level}"
        )

        return payload

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Dashboard Payload Builder test..."
    )

    # -----------------------------------------------------
    # SYNTHETIC INPUT DATA
    # -----------------------------------------------------

    fusion_report = {

        "crowd_state": "DANGEROUS",

        "fusion_risk": "SEVERE",

        "fusion_score": 7.8
    }

    risk_report = {

        "crowd_criticality_index": 8.3,

        "risk_level": "CRITICAL",

        "emergency_dispatch_required": True
    }

    outstroke_report = {

        "outstroke_probability": 0.87,

        "outstroke_risk": "CRITICAL",

        "early_warning": True,

        "estimated_collapse_window":
            "30-90 seconds"
    }

    resonance_metrics = {

        "resonance_score": 8.1,

        "resonance_probability": 0.91
    }

    turbulence_metrics = {

        "turbulence_score": 7.2,

        "crowd_instability_index": 6.8
    }

    motion_metrics = {

        "mean_velocity": 4.5,

        "dominant_direction": 84
    }

    # -----------------------------------------------------
    # RUN BUILDER
    # -----------------------------------------------------

    builder = DashboardPayloadBuilder()

    result = builder.build_payload(

        fusion_report,

        risk_report,

        outstroke_report,

        resonance_metrics,

        turbulence_metrics,

        motion_metrics
    )

    print(
        "\n========== DASHBOARD PAYLOAD ==========\n"
    )

    for key, value in result.items():

        print(f"{key}: {value}")