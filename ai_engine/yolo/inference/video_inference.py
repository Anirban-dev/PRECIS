# ai_engine/yolo/inference/video_inference.py

import cv2
import json
from pathlib import Path
from datetime import datetime

from ultralytics import YOLO

# =========================================================
# CONFIGURATION
# =========================================================

MODEL_PATH = "ai_engine/yolo/weights/yolov8n.pt"

VIDEO_PATH = "datasets/sample_videos/crowd_video.mp4"

OUTPUT_VIDEO_DIR = "ai_engine/yolo/outputs/videos"

OUTPUT_JSON_DIR = "ai_engine/yolo/outputs/json"

CONFIDENCE_THRESHOLD = 0.4

# =========================================================
# CREATE OUTPUT DIRECTORIES
# =========================================================

Path(OUTPUT_VIDEO_DIR).mkdir(parents=True, exist_ok=True)

Path(OUTPUT_JSON_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# LOAD YOLO MODEL
# =========================================================

print("\n[INFO] Loading YOLO model...\n")

model = YOLO(MODEL_PATH)

print("[INFO] YOLO model loaded successfully.\n")

# =========================================================
# VIDEO INFERENCE FUNCTION
# =========================================================

def video_inference(video_path: str):

    # -----------------------------------------------------
    # OPEN VIDEO
    # -----------------------------------------------------

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(
            f"[ERROR] Unable to open video: {video_path}"
        )

    # -----------------------------------------------------
    # VIDEO PROPERTIES
    # -----------------------------------------------------

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = int(cap.get(cv2.CAP_PROP_FPS))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # -----------------------------------------------------
    # OUTPUT FILES
    # -----------------------------------------------------

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_video_path = (
        f"{OUTPUT_VIDEO_DIR}/output_{timestamp}.mp4"
    )

    output_json_path = (
        f"{OUTPUT_JSON_DIR}/video_result_{timestamp}.json"
    )

    # -----------------------------------------------------
    # VIDEO WRITER
    # -----------------------------------------------------

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        output_video_path,
        fourcc,
        fps,
        (frame_width, frame_height)
    )

    # -----------------------------------------------------
    # PROCESS VIDEO
    # -----------------------------------------------------

    frame_number = 0

    total_person_count = 0

    video_results = []

    print("\n========================================")
    print("STARTING VIDEO INFERENCE")
    print("========================================\n")

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_number += 1

        print(
            f"[INFO] Processing frame "
            f"{frame_number}/{total_frames}"
        )

        # -------------------------------------------------
        # YOLO PREDICTION
        # -------------------------------------------------

        results = model.predict(
            source=frame,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        result = results[0]

        frame_person_count = 0

        frame_detections = []

        # -------------------------------------------------
        # PARSE DETECTIONS
        # -------------------------------------------------

        for box in result.boxes:

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            confidence = float(box.conf[0])

            # ONLY PERSON CLASS
            if class_name != "person":
                continue

            frame_person_count += 1

            total_person_count += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detection = {
                "class": class_name,
                "confidence": round(confidence, 2),
                "bbox": [x1, y1, x2, y2]
            }

            frame_detections.append(detection)

            # ---------------------------------------------
            # DRAW BOUNDING BOX
            # ---------------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"{class_name} {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        # -------------------------------------------------
        # DISPLAY PERSON COUNT
        # -------------------------------------------------

        cv2.putText(
            frame,
            f"Persons: {frame_person_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # -------------------------------------------------
        # SAVE FRAME TO OUTPUT VIDEO
        # -------------------------------------------------

        out.write(frame)

        # -------------------------------------------------
        # STORE FRAME RESULT
        # -------------------------------------------------

        frame_result = {
            "frame_number": frame_number,
            "person_count": frame_person_count,
            "detections": frame_detections
        }

        video_results.append(frame_result)

        # -------------------------------------------------
        # OPTIONAL LIVE DISPLAY
        # -------------------------------------------------

        cv2.imshow("PRECIS - Video Inference", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # =====================================================
    # RELEASE RESOURCES
    # =====================================================

    cap.release()

    out.release()

    cv2.destroyAllWindows()

    # =====================================================
    # FINAL OUTPUT JSON
    # =====================================================

    final_output = {
        "status": "completed",
        "timestamp": timestamp,
        "input_video": video_path,
        "output_video": output_video_path,
        "total_frames_processed": frame_number,
        "total_person_detections": total_person_count,
        "results": video_results
    }

    # =====================================================
    # SAVE JSON REPORT
    # =====================================================

    with open(output_json_path, "w") as json_file:
        json.dump(final_output, json_file, indent=4)

    print("\n========================================")
    print("VIDEO INFERENCE COMPLETED")
    print("========================================\n")

    print(f"[INFO] Output Video Saved: {output_video_path}")

    print(f"[INFO] JSON Report Saved: {output_json_path}")

    return final_output

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    try:

        video_inference(VIDEO_PATH)

    except Exception as e:

        print(f"\n[ERROR] {e}\n")