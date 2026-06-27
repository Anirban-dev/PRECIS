# cv_engine/preprocessing/video_loader.py

import cv2
import logging
from pathlib import Path

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("video-loader")

# =========================================================
# VIDEO LOADER ENGINE
# =========================================================

class VideoLoader:

    def __init__(self):
        logger.info(
            "Initializing Video Loading Engine..."
        )

    # =====================================================
    # GET VIDEO METADATA
    # =====================================================

    def get_metadata(self, video_path):
        """
        Extracts comprehensive metadata from a video file without reading frames.
        """
        logger.info(f"Retrieving metadata for: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Unable to open video: {video_path}")

        # Extract native properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Decode FourCC codec code back to string
        fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])

        # Calculate duration
        duration_seconds = total_frames / fps if fps > 0 else 0.0

        cap.release()

        metadata = {
            "video_path": str(video_path),
            "dimensions": {"width": width, "height": height},
            "fps": round(fps, 2),
            "total_frames": total_frames,
            "codec": codec if codec.strip() else "Unknown",
            "duration_seconds": round(duration_seconds, 2)
        }
        
        return metadata

    # =====================================================
    # STREAM FRAMES (GENERATOR)
    # =====================================================

    def stream_frames(self, video_path, start_frame=0, end_frame=None):
        """
        Yields frames sequentially using a generator to optimize memory.
        
        Parameters:
        -----------------------------------------------
        video_path  : path of input video
        start_frame : index of the frame to start reading from
        end_frame   : optional index to stop reading frames
        """
        logger.info(f"Streaming video frames from: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Unable to open video stream: {video_path}")

        # Set starting frame position if requested
        if start_frame > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            logger.info(f"Seeking stream start point to frame index: {start_frame}")

        current_frame = start_frame

        try:
            while True:
                if end_frame is not None and current_frame >= end_frame:
                    logger.info(f"Reached targeted end frame index: {end_frame}")
                    break

                ret, frame = cap.read()
                if not ret:
                    break

                # Yield the frame index along with the actual BGR frame array
                yield current_frame, frame
                current_frame += 1
                
        finally:
            cap.release()
            logger.info("Video stream connection closed cleanly.")

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    VIDEO_PATH = "datasets/sample_videos/crowd_video.mp4"

    try:
        loader = VideoLoader()

        # -------------------------------------------------
        # METADATA TEST
        # -------------------------------------------------
        metadata_report = loader.get_metadata(VIDEO_PATH)

        print("\n========== VIDEO METADATA REPORT ==========\n")
        for key, value in metadata_report.items():
            print(f"{key}: {value}")

        # -------------------------------------------------
        # STREAM SAMPLES TEST
        # -------------------------------------------------
        print("\n========== STREAMING TRIAL (FIRST 5 FRAMES) ==========\n")
        
        frame_generator = loader.stream_frames(VIDEO_PATH, start_frame=0, end_frame=5)
        
        for frame_idx, frame in frame_generator:
            print(f"Loaded Frame Index: {frame_idx:03d} | Matrix Shape: {frame.shape}")

    except Exception as e:
        logger.error(f"Video Loader Error: {e}")