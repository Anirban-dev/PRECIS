from datetime import datetime
import logging
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "gateway-service"
)


class GatewayService:

    def __init__(self):

        logger.info(
            "Initializing PRECIS Gateway Service..."
        )

    def process_risk_analysis(

        self,

        payload
    ):

        logger.info(
            "Processing crowd risk analysis..."
        )

        fusion_score = payload.get(
            "fusion_score",
            0.0
        )

        turbulence_score = payload.get(
            "turbulence_score",
            0.0
        )

        resonance_probability = payload.get(
            "resonance_probability",
            0.0
        )

        outstroke_probability = payload.get(
            "outstroke_probability",
            0.0
        )

        overall_risk_score = (

            fusion_score * 0.35 +

            turbulence_score * 0.25 +

            resonance_probability * 5 * 0.20 +

            outstroke_probability * 10 * 0.20
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

        emergency_dispatch = False

        if risk_level in [
            "SEVERE",
            "CRITICAL"
        ]:

            emergency_dispatch = True

        result = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "overall_risk_score":
                round(
                    overall_risk_score,
                    4
                ),

            "risk_level":
                risk_level,

            "emergency_dispatch":
                emergency_dispatch,

            "system_state":
                "ACTIVE"
        }

        logger.info(

            f"[RISK ANALYSIS] "

            f"Risk={risk_level} | "

            f"Score={overall_risk_score:.2f}"
        )

        return result

    def process_fusion(

        self,

        payload
    ):

        logger.info(
            "Running multi-modal fusion processing..."
        )

        optical_flow_score = payload.get(
            "optical_flow_score",
            0.0
        )

        audio_stress_score = payload.get(
            "audio_stress_score",
            0.0
        )

        density_score = payload.get(
            "density_score",
            0.0
        )

        turbulence_score = payload.get(
            "turbulence_score",
            0.0
        )

        fusion_score = (

            optical_flow_score * 0.30 +

            audio_stress_score * 0.20 +

            density_score * 0.20 +

            turbulence_score * 0.30
        )

        fusion_score = min(
            fusion_score,
            10.0
        )

        crowd_state = "STABLE"

        if fusion_score > 7:

            crowd_state = "CRITICAL"

        elif fusion_score > 5:

            crowd_state = "UNSTABLE"

        elif fusion_score > 3:

            crowd_state = "ELEVATED"

        result = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "fusion_score":
                round(fusion_score, 4),

            "crowd_state":
                crowd_state,

            "fusion_engine":
                "ACTIVE"
        }

        logger.info(

            f"[FUSION ENGINE] "

            f"FusionScore={fusion_score:.2f} | "

            f"CrowdState={crowd_state}"
        )

        return result

    def dispatch_emergency(

        self,

        payload
    ):

        logger.info(
            "Dispatching emergency response..."
        )

        risk_level = payload.get(
            "risk_level",
            "LOW"
        )

        location = payload.get(
            "location",
            "Unknown Zone"
        )

        shockwave_detected = payload.get(
            "shockwave_detected",
            False
        )

        responders = []

        if risk_level == "HIGH":

            responders.extend([

                "Crowd Control Unit",

                "Venue Security"
            ])

        elif risk_level == "SEVERE":

            responders.extend([

                "Police Response Unit",

                "Ambulance Dispatch",

                "Rapid Rescue Team"
            ])

        elif risk_level == "CRITICAL":

            responders.extend([

                "Police Command Center",

                "Fire Brigade",

                "Emergency Ambulance Network",

                "Nearby Hospitals",

                "Disaster Response Force"
            ])

        emergency_id = (
            f"PRECIS-ALERT-"
            f"{random.randint(1000,9999)}"
        )

        result = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "emergency_id":
                emergency_id,

            "location":
                location,

            "risk_level":
                risk_level,

            "shockwave_detected":
                shockwave_detected,

            "responders_notified":
                responders,

            "dispatch_status":
                "ACTIVE"
        }

        logger.info(

            f"[EMERGENCY DISPATCH] "

            f"Risk={risk_level} | "

            f"Location={location}"
        )

        return result