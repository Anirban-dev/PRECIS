# cv_engine/tests/test_wave_detector.py

import numpy as np
import logging
import sys
from pathlib import Path

# =========================================================
# ADD PROJECT ROOT TO PYTHON PATH
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

# =========================================================
# IMPORT WAVE DETECTOR ENGINE
# =========================================================

from cv_engine.optical_flow.crowd_wave_detector import CrowdWaveDetector

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("test-wave-detector")

# =========================================================
# TEST ENGINE
# =========================================================

class TestWaveDetector:

    def __init__(self):
        logger.info(
            "Initializing Crowd Wave Detector Test Suite..."
        )
        self.detector = CrowdWaveDetector()

    # =====================================================
    # TEST UNIFORM STEADY FLOW (NO SURGES)
    # =====================================================

    def test_steady_flow(self):
        logger.info("Running STEADY stream flow test...")

        # Create a steady, uniform stream matrix across a 30-frame sequence window
        # Shape structure representing time window sequences: (Frames, H, W, 2)
        sequence_len = 30
        flow_sequence = np.zeros((sequence_len, 480, 640, 2))
        
        # Inject constant uniform vector velocity along the X-axis
        flow_sequence[:, :, :, 0] = 1.5 

        result = self.detector.analyze_sequence(flow_sequence)

        print("\n========== STEADY FLOW RESULT ==========\n")
        for key, value in result.items():
            print(f"{key}: {value}")

        assert result["wave_detected"] is False
        assert result["severity_score"] < 0.3

    # =====================================================
    # TEST OSCILLATORY COMPRESSION WAVE (SURGE SHOCK)
    # =====================================================

    def test_compression_wave(self):
        logger.info("Running OSCILLATORY compression surge test...")

        sequence_len = 30
        flow_sequence = np.zeros((sequence_len, 480, 640, 2))

        # Build a coherent propagating sine wave along the timeline axis
        for t in range(sequence_len):
            wave_signal = np.sin(2 * np.pi * (t / 10.0)) * 5.0
            flow_sequence[t, :, :, 0] = wave_signal  # Dynamic surging shifts

        result = self.detector.analyze_sequence(flow_sequence)

        print("\n========== COMPRESSION SURGE RESULT ==========\n")
        for key, value in result.items():
            print(f"{key}: {value}")

        assert result["wave_detected"] is True
        assert "dominant_frequency" in result

    # =====================================================
    # RUN COMPLETE TEST SUITE
    # =====================================================

    def run_all_tests(self):
        logger.info("Starting complete wave detector test suite...")
        self.test_steady_flow()
        self.test_compression_wave()
        logger.info("All crowd wave detection tests completed successfully.")

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":
    try:
        tester = TestWaveDetector()
        tester.run_all_tests()
    except Exception as e:
        logger.error(f"Wave Detector Test Error: {e}")