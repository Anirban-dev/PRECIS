import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "evacuation-model-engine"
)


class EvacuationModelEngine:

    def __init__(self):

        logger.info(
            "Initializing Evacuation Modeling Engine..."
        )

    def simulate_evacuation(

        self,

        crowd_density_map,

        bottleneck_report,

        trajectory_report,

        available_exits=4
    ):

        logger.info(
            "Running crowd evacuation simulation..."
        )

        average_density = float(
            np.mean(crowd_density_map)
        )

        max_density = float(
            np.max(crowd_density_map)
        )

        total_people_estimate = int(
            np.sum(crowd_density_map) * 10
        )

        bottleneck_risk = (
            bottleneck_report.get(
                "bottleneck_risk",
                "LOW"
            )
        )

        collapse_probability = (
            bottleneck_report.get(
                "collapse_probability",
                0.0
            )
        )

        trajectory_risk = (
            trajectory_report.get(
                "trajectory_risk",
                "LOW"
            )
        )

        velocity_magnitude = (
            trajectory_report.get(
                "velocity_magnitude",
                0.0
            )
        )

        evacuation_complexity = (

            average_density * 0.30 +

            max_density * 0.25 +

            collapse_probability * 5 +

            velocity_magnitude * 0.10
        )

        evacuation_complexity = min(
            evacuation_complexity,
            10.0
        )

        exit_efficiency = max(

            1,

            available_exits * (
                1.5 - collapse_probability
            )
        )

        estimated_evacuation_time = (

            total_people_estimate /

            (exit_efficiency * 120)
        )

        estimated_evacuation_time = round(
            estimated_evacuation_time,
            2
        )

        evacuation_risk = "LOW"

        if evacuation_complexity > 7:

            evacuation_risk = "CRITICAL"

        elif evacuation_complexity > 5:

            evacuation_risk = "HIGH"

        elif evacuation_complexity > 3:

            evacuation_risk = "MODERATE"

        evacuation_status = "CONTROLLED"

        if (
            bottleneck_risk == "CRITICAL"
            or trajectory_risk == "CRITICAL"
        ):

            evacuation_status = (
                "COLLAPSE_RISK"
            )

        elif evacuation_risk == "HIGH":

            evacuation_status = (
                "UNSTABLE"
            )

        safe_exit_distribution = []

        for exit_id in range(available_exits):

            estimated_people = int(

                total_people_estimate /

                available_exits
            )

            safe_exit_distribution.append({

                "exit_id":
                    f"EXIT-{exit_id+1}",

                "assigned_people":
                    estimated_people,

                "status":
                    "ACTIVE"
            })

        emergency_protocol = []

        if evacuation_risk == "HIGH":

            emergency_protocol.extend([

                "Deploy police crowd control",

                "Open auxiliary exits",

                "Broadcast evacuation guidance",

                "Activate emergency pathways"
            ])

        elif evacuation_risk == "CRITICAL":

            emergency_protocol.extend([

                "Dispatch ambulance teams",

                "Alert nearby hospitals",

                "Enable emergency rescue corridors",

                "Deploy rapid response units",

                "Trigger emergency evacuation sirens",

                "Activate crowd steering protocols"
            ])

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "total_people_estimate":
                total_people_estimate,

            "average_density":
                round(average_density, 4),

            "max_density":
                round(max_density, 4),

            "evacuation_complexity":
                round(
                    evacuation_complexity,
                    4
                ),

            "evacuation_risk":
                evacuation_risk,

            "evacuation_status":
                evacuation_status,

            "available_exits":
                available_exits,

            "estimated_evacuation_time_minutes":
                estimated_evacuation_time,

            "safe_exit_distribution":
                safe_exit_distribution,

            "emergency_protocol":
                emergency_protocol
        }

        logger.info(

            f"[EVACUATION MODEL] "

            f"Risk={evacuation_risk} | "

            f"Status={evacuation_status} | "

            f"EvacuationTime={estimated_evacuation_time} mins"
        )

        return report


if __name__ == "__main__":

    crowd_density_map = np.random.uniform(
        1,
        9,
        (20, 20)
    )

    bottleneck_report = {

        "bottleneck_risk": "HIGH",

        "collapse_probability": 0.72
    }

    trajectory_report = {

        "trajectory_risk": "HIGH",

        "velocity_magnitude": 4.2
    }

    try:

        engine = EvacuationModelEngine()

        result = engine.simulate_evacuation(

            crowd_density_map,

            bottleneck_report,

            trajectory_report,

            available_exits=5
        )

        print(
            "\n========== EVACUATION REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Evacuation Simulation Error: {e}"
        )