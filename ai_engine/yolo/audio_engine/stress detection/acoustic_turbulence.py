import librosa
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "acoustic-turbulence-engine"
)


class AcousticTurbulenceEngine:

    def __init__(self):

        logger.info(
            "Initializing Acoustic Turbulence Engine..."
        )

    def analyze_audio(
        self,
        audio_path
    ):

        logger.info(
            f"Loading audio stream: {audio_path}"
        )

        audio, sample_rate = librosa.load(
            audio_path,
            sr=None
        )

        rms_energy = librosa.feature.rms(
            y=audio
        )[0]

        spectral_centroid = (
            librosa.feature.spectral_centroid(
                y=audio,
                sr=sample_rate
            )[0]
        )

        zero_crossing_rate = (
            librosa.feature.zero_crossing_rate(
                audio
            )[0]
        )

        average_energy = float(
            np.mean(rms_energy)
        )

        energy_variation = float(
            np.std(rms_energy)
        )

        average_centroid = float(
            np.mean(spectral_centroid)
        )

        centroid_variation = float(
            np.std(spectral_centroid)
        )

        average_zero_crossing = float(
            np.mean(zero_crossing_rate)
        )

        turbulence_score = (

            energy_variation * 4 +

            centroid_variation / 1000 +

            average_zero_crossing * 5
        )

        turbulence_score = min(
            turbulence_score,
            10.0
        )

        if turbulence_score < 2:

            turbulence_level = "CALM"

        elif turbulence_score < 4:

            turbulence_level = "ELEVATED"

        elif turbulence_score < 7:

            turbulence_level = "UNSTABLE"

        else:

            turbulence_level = "CRITICAL"

        panic_acoustics_detected = False

        if (
            turbulence_score > 6
            and average_energy > 0.08
        ):

            panic_acoustics_detected = True

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "average_energy":
                round(average_energy, 4),

            "energy_variation":
                round(energy_variation, 4),

            "average_centroid":
                round(average_centroid, 2),

            "centroid_variation":
                round(centroid_variation, 2),

            "average_zero_crossing":
                round(average_zero_crossing, 4),

            "turbulence_score":
                round(turbulence_score, 4),

            "turbulence_level":
                turbulence_level,

            "panic_acoustics_detected":
                panic_acoustics_detected
        }

        logger.info(

            f"[ACOUSTIC TURBULENCE] "

            f"Level={turbulence_level} | "

            f"Score={turbulence_score:.2f}"
        )

        return report


if __name__ == "__main__":

    AUDIO_PATH = (
        "datasets/sample_audio/crowd_audio.wav"
    )

    try:

        engine = AcousticTurbulenceEngine()

        result = engine.analyze_audio(
            AUDIO_PATH
        )

        print(
            "\n========== ACOUSTIC TURBULENCE REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Acoustic Turbulence Error: {e}"
        )