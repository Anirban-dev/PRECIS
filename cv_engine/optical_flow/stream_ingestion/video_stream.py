# cv_engine/stream_ingestion/video_stream.py

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

logger = logging.getLogger("video-stream-engine")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/video_streams"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# VIDEO STREAM ENGINE
# =========================================================

class VideoStreamEngine:

    def __init__(self, video_path):

        self.video_path = video_path

        logger.info(
            "Initializing Video Stream Engine..."
        )

    # =====================================================
    # START VIDEO STREAM
    # =====================================================

    def start_stream(
        self,
        display_stream=True,
        save_recording=False,
        resize_width=None,
        resize_height=None,
        grayscale=False
    ):

        logger.info(
            f"Opening video file: {self.video_path}"
        )

        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():

            raise Exception(
                f"Unable to open video file: "
                f"{self.video_path}"
            )

        logger.info(
            "Video stream opened successfully."
        )

        # -------------------------------------------------
        # VIDEO PROPERTIES
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

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        if fps == 0:
            fps = 30

        logger.info(
            f"Resolution: "
            f"{frame_width}x{frame_height}"
        )

        logger.info(
            f"FPS: {fps}"
        )

        logger.info(
            f"Total Frames: {total_frames}"
        )

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
                f"processed_video_{timestamp}.mp4"
            )

            output_width = (
                resize_width
                if resize_width
                else frame_width
            )

            output_height = (
                resize_height
                if resize_height
                else frame_height
            )

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            # ---------------------------------------------
            # HANDLE GRAYSCALE WRITING
            # ---------------------------------------------

            is_color = not grayscale

            video_writer = cv2.VideoWriter(
                output_video_path,
                fourcc,
                fps,
                (
                    output_width,
                    output_height
                ),
                isColor=is_color
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
            "Starting video stream processing..."
        )

        while True:

            ret, frame = cap.read()

            if not ret:

                logger.info(
                    "End of video reached."
                )

                break

            frame_count += 1

            processed_frame = frame

            # ---------------------------------------------
            # OPTIONAL RESIZE
            # ---------------------------------------------

            if (
                resize_width is not None
                and resize_height is not None
            ):

                processed_frame = cv2.resize(
                    processed_frame,
                    (
                        resize_width,
                        resize_height
                    )
                )

            # ---------------------------------------------
            # OPTIONAL GRAYSCALE
            # ---------------------------------------------

            if grayscale:

                processed_frame = cv2.cvtColor(
                    processed_frame,
                    cv2.COLOR_BGR2GRAY
                )

            # ---------------------------------------------
            # OVERLAY ANALYTICS
            # ---------------------------------------------

            if grayscale:

                display_frame = cv2.cvtColor(
                    processed_frame,
                    cv2.COLOR_GRAY2BGR
                )

            else:

                display_frame = processed_frame.copy()

            cv2.putText(
                display_frame,
                "PRECIS VIDEO STREAM",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"Frame: {frame_count}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            progress = (
                frame_count / total_frames
            ) * 100

            cv2.putText(
                display_frame,
                f"Progress: {progress:.1f}%",
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
                    "PRECIS Video Stream",
                    display_frame
                )

            # ---------------------------------------------
            # SAVE RECORDING
            # ---------------------------------------------

            if video_writer is not None:

                if grayscale:

                    video_writer.write(
                        processed_frame
                    )

                else:

                    video_writer.write(
                        processed_frame
                    )

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
            "Video stream processing completed."
        )

        return {

            "status": "success",

            "video_path": self.video_path,

            "frames_processed": frame_count,

            "recording_saved": save_recording,

            "output_video": output_video_path
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    VIDEO_PATH = (
        "datasets/sample_videos/crowd_video.mp4"
    )

    try:

        video_engine = VideoStreamEngine(
            video_path=VIDEO_PATH
        )

        result = video_engine.start_stream(

            display_stream=True,

            save_recording=False,

            resize_width=640,

            resize_height=480,

            grayscale=False
        )

        print("\n========== VIDEO STREAM REPORT ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Video Stream Error: {e}"
        )