# cv_engine/tests/test_optical_flow.py

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
# IMPORT OPTICAL FLOW ENGINE
# =========================================================

from cv_engine.optical_flow.flow_visualizer import FlowVisualizer

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("test-optical-flow")

# =========================================================
# TEST ENGINE
# =========================================================

class TestOpticalFlow:

    def __init__(self):
        logger.info(
            "Initializing Optical Flow Test Suite..."
        )
        self.processor = FlowVisualizer()

    # =====================================================
    # TEST STATIC SCENE (ZERO MOTION)
    # =====================================================

    def test_static_scene(self):
        logger.info("Running STATIC scene (zero motion) test...")

        # Create two identical frames (grayscale, 480x640)
        frame1 = np.ones((480, 640), dtype=np.uint8) * 128
        frame2 = np.ones((480, 640), dtype=np.uint8) * 128

        flow = self.processor.compute_flow(frame1, frame2)

        print("\n========== STATIC SCENE FLOW REPORT ==========\n")
        print(f"Flow Shape: {flow.shape}")
        print(f"Mean Flow Magnitude: {np.mean(np.abs(flow))}")

        # The shape must match (H, W, 2) for horizontal/vertical vectors
        assert flow.shape == (480, 640, 2)
        # Static frames should produce close to 0 motion vectors
        assert np.allclose(flow, 0, atol=1e-2)

    # =====================================================
    # TEST TRANSLATIONAL MOTION
    # =====================================================

    def test_translational_motion(self):
        logger.info("Running TRANSLATIONAL linear motion test...")

        # Frame 1: Draw a bright block at a base coordinate position
        frame1 = np.zeros((480, 640), dtype=np.uint8)
        frame1[200:250, 200:250] = 255

        # Frame 2: Shift the bright block down and right by 5 pixels
        frame2 = np.zeros((480, 640), dtype=np.uint8)
        frame2[205:255, 205:255] = 255

        flow = self.processor.compute_flow(frame1, frame2)

        # Average vector magnitudes within our local shifting field
        local_flow_x = np.mean(flow[205:245, 205:245, 0])
        local_flow_y = np.mean(flow[205:245, 205:245, 1])

        print("\n========== TRANSLATIONAL MOTION REPORT ==========\n")
        print(f"Detected Local X Displacement: {local_flow_x:.4f}")
        print(f"Detected Local Y Displacement: {local_flow_y:.4f}")

        assert flow.shape == (480, 640, 2)
        # Ensure direction signs align correctly with positive spatial shifting
        assert local_flow_x > 0
        assert local_flow_y > 0

    # =====================================================
    # RUN COMPLETE TEST SUITE
    # =====================================================

    def run_all_tests(self):
        logger.info("Starting complete optical flow test suite...")
        self.test_static_scene()
        self.test_translational_motion()
        logger.info("All optical flow tests completed successfully.")

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":
    try:
        tester = TestOpticalFlow()
        tester.run_all_tests()
    except Exception as e:
        logger.error(f"Optical Flow Test Error: {e}")