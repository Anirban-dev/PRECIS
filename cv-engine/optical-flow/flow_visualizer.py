# cv_engine/optical_flow/flow_visualizer.py

import cv2
import numpy as np
import logging
from pathlib import Path
from datetime import datetime

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("flow-visualizer")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/optical_flow"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# FLOW VISUALIZER ENGINE
# =========================================================

class FlowVisualizer:

    def __init__(self):

        logger.info(
            "Initializing Optical Flow Visualization Engine..."
        )

    # =====================================================
    # DRAW FLOW VECTORS
    # =====================================================

    def draw_flow_vectors(
        self,
        frame,
        flow,
        step=16
    ):

        """
        Draw directional motion vectors
        over the original frame.
        """

        height, width = frame.shape[:2]

        visualization_frame = frame.copy()

        # -------------------------------------------------
        # CREATE GRID POINTS
        # -------------------------------------------------

        y, x = np.mgrid[
            step // 2:height:step,
            step // 2:width:step
        ].reshape(2, -1)

        # -------------------------------------------------
        # EXTRACT FLOW VALUES
        # -------------------------------------------------

        fx, fy = flow[y, x].T

        # -------------------------------------------------
        # CREATE VECTOR LINES
        # -------------------------------------------------

        lines = np.vstack([
            x,
            y,
            x + fx,
            y + fy
        ]).T.reshape(-1, 2, 2)

        lines = np.int32(lines)

        # -------------------------------------------------
        # DRAW MOTION LINES
        # -------------------------------------------------

        for (x1, y1), (x2, y2) in lines:

            cv2.arrowedLine(
                visualization_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                1,
                tipLength=0.3
            )

            cv2.circle(
                visualization_frame,
                (x1, y1),
                1,
                (0, 0, 255),
                -1
            )

        return visualization_frame

    # =====================================================
    # DRAW CROWD FLOW DENSITY
    # =====================================================

    def draw_density_overlay(
        self,
        frame,
        magnitude
    ):

        """
        Highlight high-motion crowd regions.
        """

        normalized = cv2.normalize(
            magnitude,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        normalized = np.uint8(normalized)

        heatmap = cv2.applyColorMap(
            normalized,
            cv2.COLORMAP_JET
        )

        overlay = cv2.addWeighted(
            frame,
            0.6,
            heatmap,
            0.4,
            0
        )

        return overlay

    # =====================================================
    # DISPLAY ANALYTICS
    # =====================================================

    def draw_analytics(
        self,
        frame,
        avg_motion,
        turbulence_score=None,
        resonance_score=None
    ):

        """
        Overlay analytics text.
        """

        output = frame.copy()

        cv2.putText(
            output,
            f"Avg Motion: {avg_motion:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        if turbulence_score is not None:

            cv2.putText(
                output,
                f"Turbulence: {turbulence_score:.2f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

        if resonance_score is not None:

            cv2.putText(
                output,
                f"Resonance: {resonance_score:.2f}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        return output

    # =====================================================
    # SAVE VISUALIZATION FRAME
    # =====================================================

    def save_visualization(self, frame):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_path = (
            f"{OUTPUT_DIR}/flow_visualization_{timestamp}.jpg"
        )

        cv2.imwrite(output_path, frame)

        logger.info(
            f"Flow visualization saved: {output_path}"
        )

        return output_path

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Flow Visualizer self-test..."
    )

    # -----------------------------------------------------
    # CREATE DUMMY FRAME
    # -----------------------------------------------------

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    # -----------------------------------------------------
    # CREATE SYNTHETIC FLOW FIELD
    # -----------------------------------------------------

    synthetic_flow = np.random.randn(
        480,
        640,
        2
    ) * 2

    magnitude = np.sqrt(
        synthetic_flow[..., 0]**2
        +
        synthetic_flow[..., 1]**2
    )

    # -----------------------------------------------------
    # INITIALIZE VISUALIZER
    # -----------------------------------------------------

    visualizer = FlowVisualizer()

    # -----------------------------------------------------
    # DRAW FLOW VECTORS
    # -----------------------------------------------------

    vector_frame = visualizer.draw_flow_vectors(
        frame,
        synthetic_flow
    )

    # -----------------------------------------------------
    # ADD DENSITY OVERLAY
    # -----------------------------------------------------

    density_frame = visualizer.draw_density_overlay(
        vector_frame,
        magnitude
    )

    # -----------------------------------------------------
    # ADD ANALYTICS
    # -----------------------------------------------------

    final_frame = visualizer.draw_analytics(
        density_frame,
        avg_motion=np.mean(magnitude),
        turbulence_score=4.2,
        resonance_score=6.7
    )

    # -----------------------------------------------------
    # DISPLAY RESULT
    # -----------------------------------------------------

    cv2.imshow(
        "PRECIS Flow Visualizer",
        final_frame
    )

    visualizer.save_visualization(final_frame)

    logger.info(
        "Press Q to close visualization..."
    )

    while True:

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    