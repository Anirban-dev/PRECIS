# cv_engine/tests/test_turbulence.py

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
# IMPORT TURBULENCE ENGINE
# =========================================================

from turbulence_metrics import (
    TurbulenceMetricsEngine
)

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("test-turbulence")

# =========================================================
# TEST ENGINE
# =========================================================

class TestTurbulenceMetrics:

    def __init__(self):

        logger.info(
            "Initializing Turbulence Metrics Test Suite..."
        )

        self.engine = TurbulenceMetricsEngine()

    # =====================================================
    # TEST LOW TURBULENCE
    # =====================================================

    def test_low_turbulence(self):

        logger.info(
            "Running LOW turbulence test..."
        )

        # Simulate smooth crowd motion
        flow = np.random.normal(
            loc=0,
            scale=0.5,
            size=(480, 640, 2)
        )

        result = self.engine.calculate_metrics(flow)

        print("\n========== LOW TURBULENCE ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

        assert result["risk_level"] in [
            "LOW",
            "MEDIUM"
        ]

    # =====================================================
    # TEST MEDIUM TURBULENCE
    # =====================================================

    def test_medium_turbulence(self):

        logger.info(
            "Running MEDIUM turbulence test..."
        )

        # Simulate moderate crowd instability
        flow = np.random.normal(
            loc=0,
            scale=2.5,
            size=(480, 640, 2)
        )

        result = self.engine.calculate_metrics(flow)

        print("\n========== MEDIUM TURBULENCE ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

        assert result["risk_level"] in [
            "MEDIUM",
            "HIGH"
        ]

    # =====================================================
    # TEST HIGH TURBULENCE
    # =====================================================

    def test_high_turbulence(self):

        logger.info(
            "Running HIGH turbulence test..."
        )

        # Simulate chaotic crowd movement
        flow = np.random.normal(
            loc=0,
            scale=6.0,
            size=(480, 640, 2)
        )

        result = self.engine.calculate_metrics(flow)

        print("\n========== HIGH TURBULENCE ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

        assert result["risk_level"] in [
            "HIGH",
            "CRITICAL"
        ]

    # =====================================================
    # RUN COMPLETE TEST SUITE
    # =====================================================

    def run_all_tests(self):

        logger.info(
            "Starting complete turbulence test suite..."
        )

        self.test_low_turbulence()

        self.test_medium_turbulence()

        self.test_high_turbulence()

        logger.info(
            "All turbulence tests completed successfully."
        )

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    try:

        tester = TestTurbulenceMetrics()

        tester.run_all_tests()

    except Exception as e:

        logger.error(
            f"Turbulence Test Error: {e}"
        )