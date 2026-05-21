# ai-engine/yolo/inference/batch/batch_inference.py

from pathlib import Path
from datetime import datetime
import json

# =========================================================
# IMPORT IMAGE INFERENCE FUNCTION
# =========================================================

from ai_engine.yolo.inference.image.run_inference import run_inference

# =========================================================
# CONFIGURATION
# =========================================================

INPUT_FOLDER = "datasets/batch_images"

OUTPUT_JSON_DIR = "ai-engine/yolo/outputs/json"

SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

Path(OUTPUT_JSON_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# BATCH INFERENCE FUNCTION
# =========================================================

def batch_inference(input_folder: str):

    input_path = Path(input_folder)

    if not input_path.exists():
        raise FileNotFoundError(
            f"[ERROR] Folder not found: {input_folder}"
        )

    # -----------------------------------------------------
    # GET ALL IMAGE FILES
    # -----------------------------------------------------

    image_files = []

    for ext in SUPPORTED_EXTENSIONS:
        image_files.extend(input_path.glob(f"*{ext}"))

    if len(image_files) == 0:
        raise ValueError(
            f"[ERROR] No supported images found in {input_folder}"
        )

    # -----------------------------------------------------
    # START PROCESSING
    # -----------------------------------------------------

    print("\n========================================")
    print("STARTING BATCH INFERENCE")
    print("========================================\n")

    batch_results = []

    total_person_count = 0

    processed_images = 0

    # -----------------------------------------------------
    # PROCESS EACH IMAGE
    # -----------------------------------------------------

    for image_path in image_files:

        print(f"[INFO] Processing: {image_path.name}")

        try:

            result = run_inference(str(image_path))

            batch_results.append(result)

            total_person_count += result["person_count"]

            processed_images += 1

            print(
                f"[SUCCESS] {image_path.name} → "
                f"{result['person_count']} persons detected"
            )

        except Exception as e:

            print(
                f"[ERROR] Failed processing "
                f"{image_path.name}: {e}"
            )

    # -----------------------------------------------------
    # FINAL SUMMARY
    # -----------------------------------------------------

    final_output = {
        "status": "completed",
        "timestamp": datetime.utcnow().isoformat(),
        "total_images_processed": processed_images,
        "total_persons_detected": total_person_count,
        "results": batch_results
    }

    # -----------------------------------------------------
    # SAVE JSON REPORT
    # -----------------------------------------------------

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_json_path = (
        f"{OUTPUT_JSON_DIR}/batch_result_{timestamp}.json"
    )

    with open(output_json_path, "w") as json_file:
        json.dump(final_output, json_file, indent=4)

    print("\n========================================")
    print("BATCH INFERENCE COMPLETED")
    print("========================================\n")

    print(f"[INFO] Total Images Processed: {processed_images}")

    print(f"[INFO] Total Persons Detected: {total_person_count}")

    print(f"[INFO] JSON Report Saved: {output_json_path}")

    return final_output

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    try:

        batch_inference(INPUT_FOLDER)

    except Exception as e:

        print(f"\n[ERROR] {e}\n")