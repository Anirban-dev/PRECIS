# cv_engine/stream_ingestion/webcam_stream.py

import cv2
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

logger = logging.getLogger("webcam-stream-engine")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/webcam_recordings"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# WEBCAM STREAM ENGINE
# =========================================================

class WebcamStreamEngine:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index

        logger.info(
            "Initializing Webcam Stream Engine..."
        )

    # =====================================================
    # START WEBCAM STREAM
    # =====================================================

    def start_stream(
        self,
        save_recording=False,
        display_stream=True
    ):

        logger.info(
            f"Connecting to webcam index: "
            f"{self.camera_index}"
        )

        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():

            raise Exception(
                f"Unable to access webcam: "
                f"{self.camera_index}"
            )

        logger.info(
            "Webcam stream connected successfully."
        )

        # -------------------------------------------------
        # CAMERA PROPERTIES
        # -------------------------------------------------

        frame_width = int(
            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        frame_height = int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        fps = int(
            cap.get(cv2.CAP_PROP_FPS)
        )

        if fps == 0:
            fps = 30

        # -------------------------------------------------
        # OPTIONAL RECORDING SETUP
        # -------------------------------------------------

        video_writer = None

        output_video_path = None

        if save_recording:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            output_video_path = (
                f"{OUTPUT_DIR}/"
                f"webcam_recording_{timestamp}.mp4"
            )

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            video_writer = cv2.VideoWriter(
                output_video_path,
                fourcc,
                fps,
                (frame_width, frame_height)
            )

            logger.info(
                f"Recording enabled: "
                f"{output_video_path}"
            )

        # -------------------------------------------------
        # STREAM LOOP
        # -------------------------------------------------

        frame_count = 0

        logger.info(
            "Starting webcam stream processing..."
        )

        while True:

            ret, frame = cap.read()

            if not ret:

                logger.warning(
                    "Unable to fetch webcam frame."
                )

                break

            frame_count += 1

            # ---------------------------------------------
            # ANALYTICS OVERLAY
            # ---------------------------------------------

            cv2.putText(
                frame,
                "PRECIS WEBCAM LIVE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Frame: {frame_count}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            cv2.putText(
                frame,
                f"Time: {current_time}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            # ---------------------------------------------
            # DISPLAY STREAM
            # ---------------------------------------------

            if display_stream:

                cv2.imshow(
                    "PRECIS Webcam Stream",
                    frame
                )

            # ---------------------------------------------
            # SAVE RECORDING
            # ---------------------------------------------

            if video_writer is not None:

                video_writer.write(frame)

            # ---------------------------------------------
            # EXIT KEY
            # ---------------------------------------------

            key = cv2.waitKey(1)

            if key & 0xFF == ord("q"):

                logger.info(
                    "Manual stream stop triggered."
                )

                break

        # -------------------------------------------------
        # RELEASE RESOURCES
        # -------------------------------------------------

        cap.release()

        if video_writer is not None:

            video_writer.release()

        cv2.destroyAllWindows()

        logger.info(
            "Webcam stream stopped successfully."
        )

        return {

            "status": "success",

            "frames_processed": frame_count,

            "recording_saved": save_recording,

            "output_video": output_video_path
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    try:

        webcam_engine = WebcamStreamEngine(
            camera_index=0
        )

        result = webcam_engine.start_stream(

            save_recording=False,

            display_stream=True
        )

        print("\n========== WEBCAM REPORT ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Webcam Stream Error: {e}"
        )