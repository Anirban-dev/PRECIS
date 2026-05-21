# services/ai_service/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import uuid

# =========================================================
# IMPORT YOLO INFERENCE FUNCTION
# =========================================================

from ai_engine.yolo.inference.run_inference import run_inference

# =========================================================
# FASTAPI APP INITIALIZATION
# =========================================================

app = FastAPI(
    title="PRECIS AI Service",
    description="Crowd Detection & AI Inference API",
    version="1.0.0"
)

# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_DIR = "temp_uploads"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def health_check():

    return {
        "status": "running",
        "service": "PRECIS AI Service",
        "message": "AI inference service is active"
    }

# =========================================================
# DETECTION ENDPOINT
# =========================================================

@app.post("/detect")
async def detect_crowd(file: UploadFile = File(...)):

    try:

        # -------------------------------------------------
        # VALIDATE FILE TYPE
        # -------------------------------------------------

        allowed_extensions = [".jpg", ".jpeg", ".png"]

        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in allowed_extensions:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Unsupported file format"
                }
            )

        # -------------------------------------------------
        # CREATE UNIQUE FILE NAME
        # -------------------------------------------------

        unique_filename = f"{uuid.uuid4()}{file_extension}"

        saved_file_path = f"{UPLOAD_DIR}/{unique_filename}"

        # -------------------------------------------------
        # SAVE UPLOADED FILE
        # -------------------------------------------------

        with open(saved_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -------------------------------------------------
        # RUN YOLO INFERENCE
        # -------------------------------------------------

        result = run_inference(saved_file_path)

        # -------------------------------------------------
        # RETURN RESPONSE
        # -------------------------------------------------

        return JSONResponse(
            status_code=200,
            content=result
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
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )