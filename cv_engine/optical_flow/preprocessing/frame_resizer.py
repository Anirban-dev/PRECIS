# cv_engine/preprocessing/frame_resizer.py

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

logger = logging.getLogger("frame-resizer")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/resized_frames"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# FRAME RESIZER ENGINE
# =========================================================

class FrameResizer:

    def __init__(self):

        logger.info(
            "Initializing Frame Resizer Engine..."
        )

    # =====================================================
    # RESIZE SINGLE IMAGE
    # =====================================================

    def resize_image(
        self,
        image_path,
        width=640,
        height=480,
        keep_aspect_ratio=False
    ):

        logger.info(
            f"Loading image: {image_path}"
        )

        image = cv2.imread(image_path)

        if image is None:

            raise Exception(
                f"Unable to load image: {image_path}"
            )

        original_height, original_width = image.shape[:2]

        # -------------------------------------------------
        # KEEP ASPECT RATIO
        # -------------------------------------------------

        if keep_aspect_ratio:

            aspect_ratio = original_width / original_height

            if width / height > aspect_ratio:

                width = int(height * aspect_ratio)

            else:

                height = int(width / aspect_ratio)

        # -------------------------------------------------
        # RESIZE IMAGE
        # -------------------------------------------------

        resized_image = cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA
        )

        # -------------------------------------------------
        # SAVE OUTPUT
        # -------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        image_name = Path(image_path).stem

        output_path = (
            f"{OUTPUT_DIR}/"
            f"{image_name}_{width}x{height}_{timestamp}.jpg"
        )

        cv2.imwrite(
            output_path,
            resized_image
        )

        logger.info(
            f"Resized image saved: {output_path}"
        )

        return {

            "status": "success",

            "input_image": image_path,

            "output_image": output_path,

            "original_size": {
                "width": original_width,
                "height": original_height
            },

            "resized_dimensions": {
                "width": width,
                "height": height
            }
        }

    # =====================================================
    # RESIZE VIDEO FRAMES
    # =====================================================

    def resize_video_frames(
        self,
        video_path,
        width=640,
        height=480,
        frame_skip=20,
        keep_aspect_ratio=False
    ):

        logger.info(
            f"Opening video stream: {video_path}"
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
            f"{OUTPUT_DIR}/video_resize_{timestamp}"
        )

        Path(output_folder).mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "Starting video frame resizing..."
        )

        # -------------------------------------------------
        # VIDEO LOOP
        # -------------------------------------------------

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if frame_count % frame_skip == 0:

                original_height, original_width = frame.shape[:2]

                resized_width = width
                resized_height = height

                # -----------------------------------------
                # KEEP ASPECT RATIO
                # -----------------------------------------

                if keep_aspect_ratio:

                    aspect_ratio = (
                        original_width / original_height
                    )

                    if width / height > aspect_ratio:

                        resized_width = int(
                            height * aspect_ratio
                        )

                    else:

                        resized_height = int(
                            width / aspect_ratio
                        )

                # -----------------------------------------
                # RESIZE FRAME
                # -----------------------------------------

                resized_frame = cv2.resize(
                    frame,
                    (
                        resized_width,
                        resized_height
                    ),
                    interpolation=cv2.INTER_AREA
                )

                # -----------------------------------------
                # SAVE FRAME
                # -----------------------------------------

                frame_path = (
                    f"{output_folder}/"
                    f"frame_{saved_count:05d}.jpg"
                )

                cv2.imwrite(
                    frame_path,
                    resized_frame
                )

                logger.info(
                    f"Saved resized frame: {frame_path}"
                )

                saved_count += 1

            frame_count += 1

        # -------------------------------------------------
        # RELEASE VIDEO
        # -------------------------------------------------

        cap.release()

        logger.info(
            "Video frame resizing completed."
        )

        return {

            "status": "success",

            "video_path": video_path,

            "frames_processed": frame_count,

            "frames_saved": saved_count,

            "output_directory": output_folder,

            "resize_dimensions": {
                "width": width,
                "height": height
            }
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    IMAGE_PATH = "datasets/sample_images/crowd.jpg"

    VIDEO_PATH = "datasets/sample_videos/crowd_video.mp4"

    try:

        resizer = FrameResizer()

        # -------------------------------------------------
        # IMAGE TEST
        # -------------------------------------------------

        image_result = resizer.resize_image(

            image_path=IMAGE_PATH,

            width=800,

            height=600,

            keep_aspect_ratio=True
        )

        print("\n========== IMAGE RESIZE REPORT ==========\n")

        for key, value in image_result.items():

            print(f"{key}: {value}")

        # -------------------------------------------------
        # VIDEO TEST
        # -------------------------------------------------

        video_result = resizer.resize_video_frames(

            video_path=VIDEO_PATH,

            width=640,

            height=480,

            frame_skip=30,

            keep_aspect_ratio=True
        )

        print("\n========== VIDEO RESIZE REPORT ==========\n")

        for key, value in video_result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Frame Resizer Error: {e}"
        )