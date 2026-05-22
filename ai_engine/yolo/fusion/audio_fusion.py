import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("audio-fusion-engine")


class AudioFusionEngine:

    def __init__(self):

        logger.info(
            "Initializing Audio Fusion Engine..."
        )

    def fuse_audio_intelligence(

        self,

        pitch_report,

        acoustic_report,

        scream_report=None
    ):

        logger.info(
            "Running multi-layer acoustic fusion..."
        )

        pitch_drift_score = (
            pitch_report.get(
                "pitch_drift_score",
                0.0
            )
        )

        stress_level = (
            pitch_report.get(
                "stress_level",
                "CALM"
            )
        )

        screaming_detected = (
            pitch_report.get(
                "screaming_detected",
                False
            )
        )

        turbulence_score = (
            acoustic_report.get(
                "turbulence_score",
                0.0
            )
        )

        turbulence_level = (
            acoustic_report.get(
                "turbulence_level",
                "CALM"
            )
        )

        panic_acoustics_detected = (
            acoustic_report.get(
                "panic_acoustics_detected",
                False
            )
        )

        scream_probability = 0.0

        if scream_report:

            scream_probability = (
                scream_report.get(
                    "scream_probability",
                    0.0
                )
            )

        fusion_score = (

            pitch_drift_score * 3 +

            turbulence_score * 0.5 +

            scream_probability * 2
        )

        if screaming_detected:

            fusion_score += 1.5

        if panic_acoustics_detected:

            fusion_score += 1.0

        fusion_score = min(
            fusion_score,
            10.0
        )

        if fusion_score < 2:

            audio_risk = "CALM"

        elif fusion_score < 4:

            audio_risk = "ELEVATED"

        elif fusion_score < 7:

            audio_risk = "HIGH_STRESS"

        else:

            audio_risk = "PANIC"

        emergency_audio_signature = False

        if (
            audio_risk == "PANIC"
            and panic_acoustics_detected
        ):

            emergency_audio_signature = True

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "pitch_drift_score":
                round(
                    pitch_drift_score,
                    4
                ),

            "turbulence_score":
                round(
                    turbulence_score,
                    4
                ),

            "scream_probability":
                round(
                    scream_probability,
                    4
                ),

            "stress_level":
                stress_level,

            "turbulence_level":
                turbulence_level,

            "screaming_detected":
                screaming_detected,

            "panic_acoustics_detected":
                panic_acoustics_detected,

            "fusion_score":
                round(
                    fusion_score,
                    4
                ),

            "audio_risk":
                audio_risk,

            "emergency_audio_signature":
                emergency_audio_signature
        }

        logger.info(

            f"[AUDIO FUSION] "

            f"Risk={audio_risk} | "

            f"FusionScore={fusion_score:.2f}"
        )

        return report


if __name__ == "__main__":

    pitch_report = {

        "pitch_drift_score": 0.24,

        "stress_level": "HIGH_STRESS",

        "screaming_detected": True
    }

    acoustic_report = {

        "turbulence_score": 7.3,

        "turbulence_level": "CRITICAL",

        "panic_acoustics_detected": True
    }

    scream_report = {

        "scream_probability": 0.81
    }

    try:

        engine = AudioFusionEngine()

        result = engine.fuse_audio_intelligence(

            pitch_report,

            acoustic_report,

            scream_report
        )

        print(
            "\n========== AUDIO FUSION REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Audio Fusion Error: {e}"
        )