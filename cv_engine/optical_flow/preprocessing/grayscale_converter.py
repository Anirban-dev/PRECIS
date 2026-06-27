# cv_engine/preprocessing/grayscale_converter.py

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

logger = logging.getLogger("grayscale-converter")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/grayscale_frames"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# GRAYSCALE CONVERTER ENGINE
# =========================================================

class GrayscaleConverter:

    def __init__(self):

        logger.info(
            "Initializing Grayscale Conversion Engine..."
        )

    # =====================================================
    # CONVERT SINGLE IMAGE
    # =====================================================

    def convert_image(
        self,
        image_path,
        save_output=True
    ):

        logger.info(
            f"Loading image: {image_path}"
        )

        image = cv2.imread(image_path)

        if image is None:

            raise Exception(
                f"Unable to read image: {image_path}"
            )

        # -------------------------------------------------
        # CONVERT TO GRAYSCALE
        # -------------------------------------------------

        grayscale_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        output_path = None

        # -------------------------------------------------
        # SAVE OUTPUT
        # -------------------------------------------------

        if save_output:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            image_name = Path(image_path).stem

            output_path = (
                f"{OUTPUT_DIR}/"
                f"{image_name}_gray_{timestamp}.jpg"
            )

            cv2.imwrite(
                output_path,
                grayscale_image
            )

            logger.info(
                f"Grayscale image saved: {output_path}"
            )

        return {

            "status": "success",

            "input_image": image_path,

            "output_image": output_path,

            "shape": grayscale_image.shape
        }

    # =====================================================
    # CONVERT VIDEO FRAMES
    # =====================================================

    def convert_video_frames(
        self,
        video_path,
        frame_skip=20
    ):

        logger.info(
            f"Opening video: {video_path}"
        )

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():

            raise Exception(
                f"Unable to open video: {video_path}"
            )

        frame_count = 0

        saved_count = 0

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_folder = (
            f"{OUTPUT_DIR}/video_gray_{timestamp}"
        )

        Path(output_folder).mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "Starting grayscale frame conversion..."
        )

        # -------------------------------------------------
        # VIDEO LOOP
        # -------------------------------------------------

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if frame_count % frame_skip == 0:

                # -----------------------------------------
                # CONVERT FRAME
                # -----------------------------------------

                gray_frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

                # -----------------------------------------
                # SAVE FRAME
                # -----------------------------------------

                frame_path = (
                    f"{output_folder}/"
                    f"gray_frame_{saved_count:05d}.jpg"
                )

                cv2.imwrite(
                    frame_path,
                    gray_frame
                )

                logger.info(
                    f"Saved grayscale frame: {frame_path}"
                )

                saved_count += 1

            frame_count += 1

        # -------------------------------------------------
        # RELEASE VIDEO
        # -------------------------------------------------

        cap.release()

        logger.info(
            "Video grayscale conversion completed."
        )

        return {

            "status": "success",

            "video_path": video_path,

            "frames_processed": frame_count,

            "grayscale_frames_saved": saved_count,

            "output_directory": output_folder
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    IMAGE_PATH = "datasets/sample_images/crowd.jpg"

    VIDEO_PATH = "datasets/sample_videos/crowd_video.mp4"

    try:

        converter = GrayscaleConverter()

        # -------------------------------------------------
        # IMAGE TEST
        # -------------------------------------------------

        image_result = converter.convert_image(
            IMAGE_PATH
        )

        print("\n========== IMAGE RESULT ==========\n")

        for key, value in image_result.items():

            print(f"{key}: {value}")

        # -------------------------------------------------
        # VIDEO TEST
        # -------------------------------------------------

        video_result = converter.convert_video_frames(
            VIDEO_PATH,
            frame_skip=30
        )

        print("\n========== VIDEO RESULT ==========\n")

        for key, value in video_result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Grayscale Conversion Error: {e}"
        )