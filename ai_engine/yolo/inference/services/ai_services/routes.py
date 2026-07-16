# services/ai_service/routes.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from pathlib import Path
import shutil
import uuid

# =========================================================
# IMPORT YOLO INFERENCE
# =========================================================

from ai_engine.yolo.inference.run_inference import run_inference

# =========================================================
# ROUTER INITIALIZATION
# =========================================================

router = APIRouter()

# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_DIR = "temp_uploads"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# =========================================================
# HEALTH CHECK ROUTE
# =========================================================

@router.get("/")
def health_check():

    return {
        "status": "running",
        "service": "PRECIS AI Service",
        "message": "Routes working successfully"
    }

# =========================================================
# DETECTION ROUTE
# =========================================================

@router.post("/detect")
async def detect_crowd(file: UploadFile = File(...)):

    try:

        # -------------------------------------------------
        # VALIDATE FILE EXTENSION
        # -------------------------------------------------

        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in ALLOWED_EXTENSIONS:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Unsupported file format"
                }
            )

        # -------------------------------------------------
        # GENERATE UNIQUE FILE NAME
        # -------------------------------------------------

        unique_filename = f"{uuid.uuid4()}{file_extension}"

        saved_file_path = f"{UPLOAD_DIR}/{unique_filename}"

        # -------------------------------------------------
        # SAVE FILE LOCALLY
        # -------------------------------------------------

        with open(saved_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -------------------------------------------------
        # RUN YOLO INFERENCE
        # -------------------------------------------------

        inference_result = run_inference(saved_file_path)

        # -------------------------------------------------
        # RETURN RESPONSE
        # -------------------------------------------------

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": inference_result
            }
        )

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

# =========================================================
# VIDEO DETECTION PLACEHOLDER
# =========================================================

@router.post("/detect/video")
async def detect_video():

    return {
        "status": "pending",
        "message": "Video inference route coming soon"
    }

# =========================================================
# BATCH DETECTION PLACEHOLDER
# =========================================================

@router.post("/detect/batch")
async def detect_batch():

    return {
        "status": "pending",
        "message": "Batch inference route coming soon"
    }