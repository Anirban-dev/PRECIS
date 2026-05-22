# cv_engine/optical_flow/optical_flow.py

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

logger = logging.getLogger("optical-flow-engine")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/optical_flow"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# OPTICAL FLOW ENGINE
# =========================================================

class OpticalFlowEngine:

    def __init__(self):

        logger.info("Initializing Optical Flow Engine...")

    # =====================================================
    # PROCESS VIDEO
    # =====================================================

    def process_video(self, video_path: str):

        logger.info(f"Opening video stream: {video_path}")

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise Exception(f"Unable to open video: {video_path}")

        # -------------------------------------------------
        # READ FIRST FRAME
        # -------------------------------------------------

        ret, first_frame = cap.read()

        if not ret:
            raise Exception("Unable to read initial frame.")

        previous_gray = cv2.cvtColor(
            first_frame,
            cv2.COLOR_BGR2GRAY
        )

        # -------------------------------------------------
        # VIDEO PROPERTIES
        # -------------------------------------------------

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_video_path = (
            f"{OUTPUT_DIR}/optical_flow_{timestamp}.mp4"
        )

        # -------------------------------------------------
        # VIDEO WRITER
        # -------------------------------------------------

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        out = cv2.VideoWriter(
            output_video_path,
            fourcc,
            fps,
            (frame_width, frame_height)
        )

        logger.info("Starting optical flow computation...")

        frame_count = 0

        # =================================================
        # PROCESS LOOP
        # =================================================

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            current_gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            # ---------------------------------------------
            # CALCULATE OPTICAL FLOW
            # ---------------------------------------------

            flow = cv2.calcOpticalFlowFarneback(
                previous_gray,
                current_gray,
                None,
                pyr_scale=0.5,
                levels=3,
                winsize=15,
                iterations=3,
                poly_n=5,
                poly_sigma=1.2,
                flags=0
            )

            # ---------------------------------------------
            # CONVERT FLOW TO VISUAL FORMAT
            # ---------------------------------------------

            magnitude, angle = cv2.cartToPolar(
                flow[..., 0],
                flow[..., 1]
            )

            hsv = np.zeros_like(frame)

            hsv[..., 1] = 255

            hsv[..., 0] = angle * 180 / np.pi / 2

            hsv[..., 2] = cv2.normalize(
                magnitude,
                None,
                0,
                255,
                cv2.NORM_MINMAX
            )

            optical_flow_visual = cv2.cvtColor(
                hsv,
                cv2.COLOR_HSV2BGR
            )

            # ---------------------------------------------
            # OVERLAY TEXT
            # ---------------------------------------------

            avg_motion = np.mean(magnitude)

            cv2.putText(
                optical_flow_visual,
                f"Frame: {frame_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            cv2.putText(
                optical_flow_visual,
                f"Avg Motion: {avg_motion:.2f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # ---------------------------------------------
            # DISPLAY OUTPUT
            # ---------------------------------------------

            cv2.imshow(
                "PRECIS - Optical Flow Analysis",
                optical_flow_visual
            )

            # ---------------------------------------------
            # SAVE OUTPUT VIDEO
            # ---------------------------------------------

            out.write(optical_flow_visual)

            # ---------------------------------------------
            # UPDATE FRAME
            # ---------------------------------------------

            previous_gray = current_gray

            # ---------------------------------------------
            # EXIT KEY
            # ---------------------------------------------

            if cv2.waitKey(1) & 0xFF == ord("q"):
                logger.info("Manual stop triggered.")
                break

        # =================================================
        # RELEASE RESOURCES
        # =================================================

        cap.release()

        out.release()

        cv2.destroyAllWindows()

        logger.info(
            f"Optical flow processing completed. "
            f"Output saved at: {output_video_path}"
        )

        return {
            "status": "success",
            "frames_processed": frame_count,
            "output_video": output_video_path
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    VIDEO_PATH = "datasets/sample_videos/crowd_video.mp4"

    try:

        engine = OpticalFlowEngine()

        result = engine.process_video(VIDEO_PATH)

        logger.info(result)

    except Exception as e:

        logger.error(f"Optical Flow Engine Error: {e}")