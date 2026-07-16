import librosa
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("pitch-drift-engine")


class PitchDriftAnalyzer:

    def __init__(self):

        logger.info(
            "Initializing Acoustic Pitch Drift Analyzer..."
        )

    def analyze_audio(
        self,
        audio_path
    ):

        logger.info(
            f"Loading audio file: {audio_path}"
        )

        audio, sample_rate = librosa.load(
            audio_path,
            sr=None
        )

        pitches, magnitudes = librosa.piptrack(
            y=audio,
            sr=sample_rate
        )

        pitch_values = []

        for i in range(pitches.shape[1]):

            index = magnitudes[:, i].argmax()

            pitch = pitches[index, i]

            if pitch > 0:

                pitch_values.append(pitch)

        if len(pitch_values) == 0:

            raise Exception(
                "No pitch values detected."
            )

        pitch_values = np.array(pitch_values)

        average_pitch = float(
            np.mean(pitch_values)
        )

        pitch_variation = float(
            np.std(pitch_values)
        )

        pitch_drift_score = float(
            pitch_variation / (
                average_pitch + 1e-6
            )
        )

        if pitch_drift_score < 0.05:

            stress_level = "CALM"

        elif pitch_drift_score < 0.12:

            stress_level = "ELEVATED"

        elif pitch_drift_score < 0.20:

            stress_level = "HIGH_STRESS"

        else:

            stress_level = "PANIC"

        screaming_detected = False

        if average_pitch > 350:

            screaming_detected = True

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "average_pitch":
                round(average_pitch, 2),

            "pitch_variation":
                round(pitch_variation, 2),

            "pitch_drift_score":
                round(pitch_drift_score, 4),

            "stress_level":
                stress_level,

            "screaming_detected":
                screaming_detected
        }

        logger.info(

            f"[PITCH ANALYSIS] "

            f"Stress={stress_level} | "

            f"PitchDrift={pitch_drift_score:.4f}"
        )

        return report


if __name__ == "__main__":

    AUDIO_PATH = (
        "datasets/sample_audio/crowd_audio.wav"
    )

    try:

        analyzer = PitchDriftAnalyzer()

        result = analyzer.analyze_audio(
            AUDIO_PATH
        )

        print(
            "\n========== PITCH DRIFT REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Pitch Drift Analysis Error: {e}"
        )