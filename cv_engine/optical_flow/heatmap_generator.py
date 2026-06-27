# cv_engine/optical_flow/heatmap_generator.py

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

logger = logging.getLogger("heatmap-generator")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/heatmaps"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# HEATMAP GENERATOR ENGINE
# =========================================================

class HeatmapGenerator:

    def __init__(self):

        logger.info(
            "Initializing Crowd Heatmap Generator..."
        )

    # =====================================================
    # GENERATE HEATMAP FROM FLOW MAGNITUDE
    # =====================================================

    def generate_heatmap(
        self,
        magnitude,
        original_frame=None,
        alpha=0.6
    ):

        """
        magnitude:
            Optical flow magnitude matrix

        original_frame:
            Original video frame (optional)

        alpha:
            Overlay blending factor
        """

        # -------------------------------------------------
        # NORMALIZE MAGNITUDE
        # -------------------------------------------------

        normalized_magnitude = cv2.normalize(
            magnitude,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        normalized_magnitude = np.uint8(
            normalized_magnitude
        )

        # -------------------------------------------------
        # APPLY COLOR MAP
        # -------------------------------------------------

        heatmap = cv2.applyColorMap(
            normalized_magnitude,
            cv2.COLORMAP_JET
        )

        # -------------------------------------------------
        # OVERLAY ON ORIGINAL FRAME
        # -------------------------------------------------

        if original_frame is not None:

            blended = cv2.addWeighted(
                original_frame,
                1 - alpha,
                heatmap,
                alpha,
                0
            )

            output_frame = blended

        else:

            output_frame = heatmap

        return output_frame

    # =====================================================
    # GENERATE RISK ZONE MASK
    # =====================================================

    def generate_risk_zones(
        self,
        magnitude,
        threshold=15
    ):

        """
        Detect high-pressure crowd zones.
        """

        # -------------------------------------------------
        # CREATE RISK MASK
        # -------------------------------------------------

        risk_mask = np.zeros_like(
            magnitude,
            dtype=np.uint8
        )

        risk_mask[magnitude > threshold] = 255

        return risk_mask

    # =====================================================
    # SAVE HEATMAP
    # =====================================================

    def save_heatmap(self, frame):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_path = (
            f"{OUTPUT_DIR}/heatmap_{timestamp}.jpg"
        )

        cv2.imwrite(output_path, frame)

        logger.info(
            f"Heatmap saved successfully: {output_path}"
        )

        return output_path

# =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    logger.info(
        "Running Heatmap Generator self-test..."
    )

    # -----------------------------------------------------
    # CREATE SYNTHETIC MOTION FIELD
    # -----------------------------------------------------

    synthetic_magnitude = np.random.rand(
        480,
        640
    ) * 25

    # -----------------------------------------------------
    # GENERATE HEATMAP
    # -----------------------------------------------------

    generator = HeatmapGenerator()

    heatmap = generator.generate_heatmap(
        synthetic_magnitude
    )

    # -----------------------------------------------------
    # DISPLAY RESULT
    # -----------------------------------------------------

    cv2.imshow(
        "PRECIS Crowd Heatmap",
        heatmap
    )

    generator.save_heatmap(heatmap)

    logger.info(
        "Press Q to close heatmap window..."
    )

    while True:

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()