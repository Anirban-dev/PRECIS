# cv_engine/report_generator.py

import json
import logging
from pathlib import Path
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("report-generator")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/risk_reports"

Path(OUTPUT_DIR).mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# REPORT GENERATOR ENGINE
# =========================================================

class ReportGenerator:

    def __init__(self):

        logger.info(
            "Initializing Crowd Intelligence Report Generator..."
        )

    # =====================================================
    # GENERATE FULL REPORT
    # =====================================================

    def generate_report(

        self,

        fusion_report,

        risk_report,

        outstroke_report,

        dashboard_payload
    ):

        """
        Generates:
        - incident analytics reports
        - risk summaries
        - emergency intelligence reports
        """

        logger.info(
            "Generating crowd intelligence report..."
        )

        # -------------------------------------------------
        # REPORT METADATA
        # -------------------------------------------------

        timestamp = datetime.utcnow().isoformat()

        report_id = (
            f"PRECIS_REPORT_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        )

        # -------------------------------------------------
        # EXECUTIVE SUMMARY
        # -------------------------------------------------

        executive_summary = {

            "report_id": report_id,

            "generated_at": timestamp,

            "system": "PRECIS / NEURAL-SHIELD",

            "report_type":
                "Predictive Crowd Intelligence Report"
        }

        # -------------------------------------------------
        # INCIDENT OVERVIEW
        # -------------------------------------------------

        incident_overview = {

            "crowd_state":
                fusion_report.get(
                    "crowd_state",
                    "UNKNOWN"
                ),

            "fusion_risk":
                fusion_report.get(
                    "fusion_risk",
                    "LOW"
                ),

            "risk_level":
                risk_report.get(
                    "risk_level",
                    "LOW"
                ),

            "outstroke_risk":
                outstroke_report.get(
                    "outstroke_risk",
                    "LOW"
                )
        }

        # -------------------------------------------------
        # CRITICAL METRICS
        # -------------------------------------------------

        critical_metrics = {

            "fusion_score":
                fusion_report.get(
                    "fusion_score",
                    0.0
                ),

            "crowd_criticality_index":
                risk_report.get(
                    "crowd_criticality_index",
                    0.0
                ),

            "outstroke_probability":
                outstroke_report.get(
                    "outstroke_probability",
                    0.0
                ),

            "resonance_probability":
                fusion_report.get(
                    "resonance_probability",
                    0.0
                ),

            "shockwave_detected":
                fusion_report.get(
                    "shockwave_detected",
                    False
                ),

            "pre_disaster_state":
                fusion_report.get(
                    "pre_disaster_state",
                    False
                )
        }

        # -------------------------------------------------
        # PREVENTIVE ACTIONS
        # -------------------------------------------------

        preventive_actions = {

            "emergency_dispatch_required":
                risk_report.get(
                    "emergency_dispatch_required",
                    False
                ),

            "recommended_actions":
                outstroke_report.get(
                    "preventive_actions",
                    []
                )
        }

        # -------------------------------------------------
        # EMERGENCY RESPONSE STATUS
        # -------------------------------------------------

        emergency_response = {

            "hospital_alert":
                False,

            "ambulance_dispatch":
                False,

            "fire_brigade_alert":
                False,

            "police_control_alert":
                False
        }

        if (
            risk_report.get("risk_level")
            in ["SEVERE", "CRITICAL"]
        ):

            emergency_response.update({

                "hospital_alert": True,

                "ambulance_dispatch": True,

                "police_control_alert": True
            })

        if (
            risk_report.get("risk_level")
            == "CRITICAL"
        ):

            emergency_response[
                "fire_brigade_alert"
            ] = True

        # -------------------------------------------------
        # DASHBOARD SNAPSHOT
        # -------------------------------------------------

        dashboard_snapshot = dashboard_payload

        # -------------------------------------------------
        # FINAL REPORT
        # -------------------------------------------------

        final_report = {

            "executive_summary":
                executive_summary,

            "incident_overview":
                incident_overview,

            "critical_metrics":
                critical_metrics,

            "preventive_actions":
                preventive_actions,

            "emergency_response":
                emergency_response,

            "dashboard_snapshot":
                dashboard_snapshot
        }

        # -------------------------------------------------
        # SAVE REPORT
        # -------------------------------------------------

        output_path = (
            f"{OUTPUT_DIR}/"
            f"{report_id}.json"
        )

        with open(output_path, "w") as report_file:

            json.dump(

                final_report,

                report_file,

                indent=4
            )

        logger.info(
            f"Report generated successfully: "
            f"{output_path}"
        )

        return {

            "status": "success",

            "report_id": report_id,

            "report_path": output_path,

            "generated_at": timestamp
        }

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Report Generator self-test..."
    )

    # -----------------------------------------------------
    # SYNTHETIC TEST DATA
    # -----------------------------------------------------

    fusion_report = {

        "crowd_state": "COLLAPSE_IMMINENT",

        "fusion_risk": "CRITICAL",

        "fusion_score": 9.2,

        "resonance_probability": 0.91,

        "shockwave_detected": True,

        "pre_disaster_state": True
    }

    risk_report = {

        "risk_level": "CRITICAL",

        "crowd_criticality_index": 9.5,

        "emergency_dispatch_required": True
    }

    outstroke_report = {

        "outstroke_risk": "CRITICAL",

        "outstroke_probability": 0.94,

        "preventive_actions": [

            "Dispatch ambulance network",

            "Alert nearby hospitals",

            "Enable emergency crowd steering"
        ]
    }

    dashboard_payload = {

        "dashboard_status": {

            "alert_status": "CRITICAL_ALERT",

            "ui_color": "red"
        }
    }

    # -----------------------------------------------------
    # RUN GENERATOR
    # -----------------------------------------------------

    generator = ReportGenerator()

    result = generator.generate_report(

        fusion_report,

        risk_report,

        outstroke_report,

        dashboard_payload
    )

    print(
        "\n========== REPORT GENERATION ==========\n"
    )

    for key, value in result.items():

        print(f"{key}: {value}")