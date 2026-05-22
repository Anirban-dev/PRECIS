# services/ai_service/schemas.py

from pydantic import BaseModel
from typing import List

# =========================================================
# BOUNDING BOX SCHEMA
# =========================================================

class BoundingBox(BaseModel):

    x1: int
    y1: int
    x2: int
    y2: int

# =========================================================
# DETECTION SCHEMA
# =========================================================

class Detection(BaseModel):

    class_name: str

    confidence: float

    bbox: BoundingBox

# =========================================================
# DETECTION RESPONSE SCHEMA
# =========================================================

class DetectionResponse(BaseModel):

    status: str

    timestamp: str

    input_image: str

    output_image: str

    person_count: int

    detections: List[Detection]

# =========================================================
# ERROR RESPONSE SCHEMA
# =========================================================

class ErrorResponse(BaseModel):

    status: str

    message: str

# =========================================================
# HEALTH CHECK RESPONSE SCHEMA
# =========================================================

class HealthCheckResponse(BaseModel):

    status: str

    service: str

    message: str

# =========================================================
# VIDEO PLACEHOLDER RESPONSE
# =========================================================

class VideoInferenceResponse(BaseModel):

    status: str

    message: str

# =========================================================
# BATCH PLACEHOLDER RESPONSE
# =========================================================

class BatchInferenceResponse(BaseModel):

    status: str

    message: str