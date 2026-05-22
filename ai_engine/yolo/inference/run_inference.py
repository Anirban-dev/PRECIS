# ai-engine/yolo/inference/run_inference.py

from ultralytics import YOLO
import cv2
from pathlib import Path
from datetime import datetime
import json

# =========================================================
# CONFIGURATION
# =========================================================

MODEL_PATH = "ai-engine/yolo/weights/yolov8n.pt"

TEST_IMAGE_PATH = "datasets/sample_images/crowd.jpg"

CONFIDENCE_THRESHOLD = 0.4

OUTPUT_DIR = "outputs"

# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# LOAD YOLO MODEL
# =========================================================

print("\n[INFO] Loading YOLO model...\n")

model = YOLO(MODEL_PATH)

print("[INFO] YOLO model loaded successfully.\n")

# =========================================================
# RUN INFERENCE FUNCTION
# =========================================================

def run_inference(image_path: str):

    # -----------------------------------------------------
    # READ IMAGE
    # -----------------------------------------------------

    frame = cv2.imread(image_path)

    if frame is None:
        raise FileNotFoundError(
            f"[ERROR] Unable to read image: {image_path}"
        )

    # -----------------------------------------------------
    # YOLO PREDICTION
    # -----------------------------------------------------

    results = model.predict(
        source=frame,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False
    )

    result = results[0]

    detections = []

    person_count = 0

    # -----------------------------------------------------
    # PARSE DETECTIONS
    # -----------------------------------------------------

    for box in result.boxes:

        class_id = int(box.cls[0])

        class_name = model.names[class_id]

        confidence = float(box.conf[0])

        # ONLY DETECT PERSONS
        if class_name != "person":
            continue

        person_count += 1

        # BOUNDING BOX COORDINATES
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detection = {
            "class": class_name,
            "confidence": round(confidence, 2),
            "bbox": [x1, y1, x2, y2]
        }

        detections.append(detection)

        # -------------------------------------------------
        # DRAW BOUNDING BOX
        # -------------------------------------------------

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # LABEL
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

    # -----------------------------------------------------
    # SAVE OUTPUT IMAGE
    # -----------------------------------------------------

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_image_path = f"{OUTPUT_DIR}/output_{timestamp}.jpg"

    cv2.imwrite(output_image_path, frame)

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    response = {
        "status": "success",
        "timestamp": timestamp,
        "input_image": image_path,
        "output_image": output_image_path,
        "person_count": person_count,
        "detections": detections
    }

    return response

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    try:

        output = run_inference(TEST_IMAGE_PATH)

        print("\n========== YOLO DETECTION RESULT ==========\n")

        print(json.dumps(output, indent=4))

        print("\n[INFO] Output image saved successfully.\n")

    except Exception as e:

        print(f"\n[ERROR] {e}\n")