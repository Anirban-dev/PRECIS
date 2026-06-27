# cv_engine/stream_ingestion/rtsp_stream.py

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

logger = logging.getLogger("rtsp-stream-engine")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/rtsp_recordings"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# RTSP STREAM ENGINE
# =========================================================

class RTSPStreamEngine:

    def __init__(self, rtsp_url):

        self.rtsp_url = rtsp_url

        logger.info(
            "Initializing RTSP Stream Engine..."
        )

    # =====================================================
    # START STREAM
    # =====================================================

    def start_stream(
        self,
        save_recording=False,
        display_stream=True
    ):

        logger.info(
            f"Connecting to RTSP stream: {self.rtsp_url}"
        )

        cap = cv2.VideoCapture(self.rtsp_url)

        if not cap.isOpened():

            raise Exception(
                f"Unable to connect to RTSP stream: "
                f"{self.rtsp_url}"
            )

        logger.info(
            "RTSP stream connected successfully."
        )

        # -------------------------------------------------
        # STREAM PROPERTIES
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
            fps = 25

        # -------------------------------------------------
        # OPTIONAL VIDEO RECORDING
        # -------------------------------------------------

        video_writer = None

        output_video_path = None

        if save_recording:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            output_video_path = (
                f"{OUTPUT_DIR}/"
                f"rtsp_recording_{timestamp}.mp4"
            )

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            video_writer = cv2.VideoWriter(
                output_video_path,
                fourcc,
                fps,
                (frame_width, frame_height)
            )

            logger.info(
                f"Recording enabled: {output_video_path}"
            )

        # -------------------------------------------------
        # STREAM LOOP
        # -------------------------------------------------

        frame_count = 0

        logger.info(
            "Starting RTSP live stream processing..."
        )

        while True:

            ret, frame = cap.read()

            if not ret:

                logger.warning(
                    "Frame read failed. "
                    "Attempting reconnect..."
                )

                break

            frame_count += 1

            # ---------------------------------------------
            # OVERLAY ANALYTICS
            # ---------------------------------------------

            cv2.putText(
                frame,
                f"PRECIS RTSP LIVE",
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

            # ---------------------------------------------
            # DISPLAY STREAM
            # ---------------------------------------------

            if display_stream:

                cv2.imshow(
                    "PRECIS RTSP Stream",
                    frame
                )

            # ---------------------------------------------
            # SAVE RECORDING
            # ---------------------------------------------

            if video_writer is not None:

                video_writer.write(frame)

            # ---------------------------------------------
            # EXIT CONDITION
            # ---------------------------------------------

            key = cv2.waitKey(1)

            if key & 0xFF == ord("q"):

                logger.info(
                    "Manual shutdown triggered."
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
            "RTSP stream stopped successfully."
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

    # -----------------------------------------------------
    # SAMPLE RTSP URL
    # -----------------------------------------------------

    RTSP_URL = (
        "rtsp://username:password@ip-address:554/stream"
    )

    try:

        stream_engine = RTSPStreamEngine(
            rtsp_url=RTSP_URL
        )

        result = stream_engine.start_stream(

            save_recording=False,

            display_stream=True
        )

        print("\n========== RTSP REPORT ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"RTSP Stream Error: {e}"
        )