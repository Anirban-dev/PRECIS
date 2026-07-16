import librosa
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("scream-detection-engine")


class ScreamDetectionEngine:

    # Screaming voice typically occupies 500–4000 Hz.
    SCREAM_FREQ_LOW = 500
    SCREAM_FREQ_HIGH = 4000

    # RMS energy threshold — screams are loud.
    ENERGY_THRESHOLD = 0.07

    # Spectral flatness: screams are tonal/narrow,
    # so flatness is low (closer to 0).
    FLATNESS_THRESHOLD = 0.15

    def __init__(self):

        logger.info(
            "Initializing Scream Detection Engine..."
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

        # ── Energy ────────────────────────────────────
        rms_energy = librosa.feature.rms(y=audio)[0]

        average_energy = float(np.mean(rms_energy))
        peak_energy = float(np.max(rms_energy))
        energy_variation = float(np.std(rms_energy))

        # ── Pitch via piptrack ─────────────────────────
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
            raise ValueError(
                "No pitch values detected in audio."
            )

        pitch_values = np.array(pitch_values)

        average_pitch = float(np.mean(pitch_values))
        peak_pitch = float(np.max(pitch_values))
        pitch_variation = float(np.std(pitch_values))

        # ── Spectral features ─────────────────────────
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio,
            sr=sample_rate
        )[0]

        spectral_flatness = librosa.feature.spectral_flatness(
            y=audio
        )[0]

        zero_crossing_rate = librosa.feature.zero_crossing_rate(
            audio
        )[0]

        average_centroid = float(np.mean(spectral_centroid))
        average_flatness = float(np.mean(spectral_flatness))
        average_zcr = float(np.mean(zero_crossing_rate))

        # ── Band energy ratio (scream frequency band) ──
        stft = np.abs(librosa.stft(audio))
        freqs = librosa.fft_frequencies(sr=sample_rate)

        band_mask = (
            (freqs >= self.SCREAM_FREQ_LOW) &
            (freqs <= self.SCREAM_FREQ_HIGH)
        )

        band_energy = float(
            np.mean(stft[band_mask, :])
        )

        total_energy = float(np.mean(stft)) + 1e-6

        band_energy_ratio = band_energy / total_energy

        # ── Scream confidence score (0–10) ─────────────
        #
        # Weighted combination of indicators:
        #   • High RMS energy          → screams are loud
        #   • High pitch               → screams are high-pitched
        #   • High pitch variation     → screams fluctuate
        #   • High band energy ratio   → energy concentrated in scream band
        #   • Low spectral flatness    → screams are tonal, not noisy
        #   • High zero-crossing rate  → rapid waveform oscillations

        energy_score = min(average_energy / self.ENERGY_THRESHOLD, 1.0) * 2.5

        pitch_score = min(average_pitch / 400.0, 1.0) * 2.0

        pitch_var_score = min(pitch_variation / 200.0, 1.0) * 1.0

        band_score = min(band_energy_ratio / 1.5, 1.0) * 2.0

        flatness_score = (
            max(0.0, self.FLATNESS_THRESHOLD - average_flatness)
            / self.FLATNESS_THRESHOLD
        ) * 1.5

        zcr_score = min(average_zcr / 0.15, 1.0) * 1.0

        scream_confidence = (
            energy_score
            + pitch_score
            + pitch_var_score
            + band_score
            + flatness_score
            + zcr_score
        )

        scream_confidence = round(min(scream_confidence, 10.0), 4)

        # ── Intensity classification ───────────────────
        if scream_confidence < 2.5:
            intensity_level = "NONE"

        elif scream_confidence < 4.5:
            intensity_level = "POSSIBLE"

        elif scream_confidence < 6.5:
            intensity_level = "LIKELY"

        elif scream_confidence < 8.5:
            intensity_level = "CONFIRMED"

        else:
            intensity_level = "EXTREME"

        # ── Hard-rule scream flag ──────────────────────
        scream_detected = (
            average_energy > self.ENERGY_THRESHOLD
            and average_pitch > 350
            and average_flatness < self.FLATNESS_THRESHOLD
        )

        # ── Build report ───────────────────────────────
        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "average_energy":
                round(average_energy, 4),

            "peak_energy":
                round(peak_energy, 4),

            "energy_variation":
                round(energy_variation, 4),

            "average_pitch":
                round(average_pitch, 2),

            "peak_pitch":
                round(peak_pitch, 2),

            "pitch_variation":
                round(pitch_variation, 2),

            "average_centroid":
                round(average_centroid, 2),

            "average_flatness":
                round(average_flatness, 4),

            "average_zero_crossing_rate":
                round(average_zcr, 4),

            "band_energy_ratio":
                round(band_energy_ratio, 4),

            "scream_confidence":
                scream_confidence,

            "intensity_level":
                intensity_level,

            "scream_detected":
                scream_detected
        }

        logger.info(
            f"[SCREAM DETECTION] "
            f"Intensity={intensity_level} | "
            f"Confidence={scream_confidence:.2f} | "
            f"Detected={scream_detected}"
        )

        return report


if __name__ == "__main__":

    AUDIO_PATH = (
        "datasets/sample_audio/crowd_audio.wav"
    )

    try:

        engine = ScreamDetectionEngine()

        result = engine.analyze_audio(AUDIO_PATH)

        print(
            "\n========== SCREAM DETECTION REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Scream Detection Error: {e}"
        )