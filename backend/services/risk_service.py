import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("risk-service")


class RiskService:

    def __init__(self):

        logger.info(
            "Initializing Risk Intelligence Service..."
        )

    def evaluate_risk(

        self,

        fusion_report,

        outstroke_report,

        bottleneck_report,

        evacuation_report
    ):

        logger.info(
            "Evaluating unified crowd risk..."
        )

        fusion_score = fusion_report.get(
            "fusion_score",
            0.0
        )

        outstroke_probability = (
            outstroke_report.get(
                "outstroke_probability",
                0.0
            )
        )

        bottleneck_score = (
            bottleneck_report.get(
                "bottleneck_score",
                0.0
            )
        )

        evacuation_complexity = (
            evacuation_report.get(
                "evacuation_complexity",
                0.0
            )
        )

        crowd_state = fusion_report.get(
            "crowd_state",
            "NORMAL"
        )

        evacuation_status = (
            evacuation_report.get(
                "evacuation_status",
                "CONTROLLED"
            )
        )

        overall_risk_score = (

            fusion_score * 0.35 +

            outstroke_probability * 10 * 0.25 +

            bottleneck_score * 0.20 +

            evacuation_complexity * 0.20
        )

        overall_risk_score = min(
            overall_risk_score,
            10.0
        )

        if overall_risk_score < 2:

            risk_level = "LOW"

        elif overall_risk_score < 4:

            risk_level = "MODERATE"

        elif overall_risk_score < 6:

            risk_level = "HIGH"

        elif overall_risk_score < 8:

            risk_level = "SEVERE"

        else:

            risk_level = "CRITICAL"

        emergency_dispatch_required = False

        if risk_level in [
            "SEVERE",
            "CRITICAL"
        ]:

            emergency_dispatch_required = True

        system_state = "STABLE"

        if crowd_state == "COLLAPSE_IMMINENT":

            system_state = "PRE_DISASTER"

        elif evacuation_status == "COLLAPSE_RISK":

            system_state = "EMERGENCY"

        recommended_response = []

        if risk_level == "HIGH":

            recommended_response.extend([

                "Increase crowd monitoring",

                "Deploy additional personnel",

                "Monitor pressure zones"
            ])

        elif risk_level == "SEVERE":

            recommended_response.extend([

                "Alert rescue teams",

                "Prepare evacuation units",

                "Notify emergency services",

                "Activate emergency monitoring"
            ])

        elif risk_level == "CRITICAL":

            recommended_response.extend([

                "Dispatch ambulances",

                "Notify nearby hospitals",

                "Alert police command center",

                "Deploy rapid response force",

                "Initiate emergency evacuation",

                "Activate disaster protocols"
            ])

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "overall_risk_score":
                round(
                    overall_risk_score,
                    4
                ),

            "risk_level":
                risk_level,

            "system_state":
                system_state,

            "crowd_state":
                crowd_state,

            "evacuation_status":
                evacuation_status,

            "emergency_dispatch_required":
                emergency_dispatch_required,

            "recommended_response":
                recommended_response
        }

        logger.info(

            f"[RISK SERVICE] "

            f"Risk={risk_level} | "

            f"Score={overall_risk_score:.2f} | "

            f"State={system_state}"
        )

        return report


if __name__ == "__main__":

    fusion_report = {

        "fusion_score": 8.4,

        "crowd_state": "COLLAPSE_IMMINENT"
    }

    outstroke_report = {

        "outstroke_probability": 0.88
    }

    bottleneck_report = {

        "bottleneck_score": 7.6
    }

    evacuation_report = {

        "evacuation_complexity": 8.2,

        "evacuation_status": "COLLAPSE_RISK"
    }

    try:

        service = RiskService()

        result = service.evaluate_risk(

            fusion_report,

            outstroke_report,

            bottleneck_report,

            evacuation_report
        )

        print(
            "\n========== RISK SERVICE REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Risk Service Error: {e}"
        )