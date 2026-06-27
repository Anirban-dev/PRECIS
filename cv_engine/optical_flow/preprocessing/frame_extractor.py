# cv_engine/preprocessing/frame_extractor.py

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

logger = logging.getLogger("frame-extractor")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/extracted_frames"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# FRAME EXTRACTION ENGINE
# =========================================================

class FrameExtractor:

    def __init__(self):

        logger.info(
            "Initializing Video Frame Extraction Engine..."
        )

    # =====================================================
    # EXTRACT FRAMES
    # =====================================================

    def extract_frames(
        self,
        video_path,
        frame_skip=30,
        resize_width=None,
        resize_height=None,
        grayscale=False
    ):

        """
        Parameters:
        -----------------------------------------------
        video_path      : path of input video
        frame_skip      : extract every nth frame
        resize_width    : optional width resize
        resize_height   : optional height resize
        grayscale       : convert frame to grayscale
        """

        logger.info(
            f"Opening video stream: {video_path}"
        )

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():

            raise Exception(
                f"Unable to open video: {video_path}"
            )

        # -------------------------------------------------
        # VIDEO INFORMATION
        # -------------------------------------------------

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        fps = int(
            cap.get(cv2.CAP_PROP_FPS)
        )

        logger.info(
            f"Total Frames: {total_frames}"
        )

        logger.info(
            f"FPS: {fps}"
        )

        # -------------------------------------------------
        # EXTRACTION LOOP
        # -------------------------------------------------

        frame_count = 0

        saved_count = 0

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        extraction_folder = (
            f"{OUTPUT_DIR}/frames_{timestamp}"
        )

        Path(extraction_folder).mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "Starting frame extraction..."
        )

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            # ---------------------------------------------
            # PROCESS EVERY nth FRAME
            # ---------------------------------------------

            if frame_count % frame_skip == 0:

                processed_frame = frame

                # -----------------------------------------
                # OPTIONAL RESIZING
                # -----------------------------------------

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

                # -----------------------------------------
                # OPTIONAL GRAYSCALE
                # -----------------------------------------

                if grayscale:

                    processed_frame = cv2.cvtColor(
                        processed_frame,
                        cv2.COLOR_BGR2GRAY
                    )

                # -----------------------------------------
                # SAVE FRAME
                # -----------------------------------------

                frame_filename = (
                    f"{extraction_folder}/"
                    f"frame_{saved_count:05d}.jpg"
                )

                cv2.imwrite(
                    frame_filename,
                    processed_frame
                )

                logger.info(
                    f"Saved frame: {frame_filename}"
                )

                saved_count += 1

            frame_count += 1

        # -------------------------------------------------
        # RELEASE VIDEO
        # -------------------------------------------------

        cap.release()

        logger.info(
            "Frame extraction completed successfully."
        )

        logger.info(
            f"Total frames extracted: {saved_count}"
        )

        return {

            "status": "success",

            "video_path": video_path,

            "total_video_frames": total_frames,

            "frames_extracted": saved_count,

            "output_directory": extraction_folder
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    VIDEO_PATH = "datasets/sample_videos/crowd_video.mp4"

    try:

        extractor = FrameExtractor()

        result = extractor.extract_frames(

            video_path=VIDEO_PATH,

            frame_skip=20,

            resize_width=640,

            resize_height=480,

            grayscale=False
        )

        print("\n========== EXTRACTION REPORT ==========\n")

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Frame Extraction Error: {e}"
        )