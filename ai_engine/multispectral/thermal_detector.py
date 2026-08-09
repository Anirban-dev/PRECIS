import logging
import os
from pathlib import Path

from ultralytics import YOLO

logger = logging.getLogger(__name__)


class ThermalDetector:

    def __init__(
        self,
        model_path=None
    ):
        default_model_path = (
            Path(__file__).resolve().parents[1] / "models" / "thermal_yolov8.pt"
        )
        configured_path = model_path or os.getenv(
            "PRECIS_THERMAL_MODEL_PATH",
            str(default_model_path)
        )
        self.model = YOLO(configured_path)

    def detect(
        self,
        frame,
        confidence=0.35
    ):
        # Optimized: Explicitly passing imgsz=640 to match camera resolution
        # and using stream=True for optimized video framing pipelines.
        results = self.model.predict(
            source=frame,
            conf=confidence,
            imgsz=640,
            verbose=False,
            stream=True
        )

        detections = []

        for result in results:
            if len(result.boxes) == 0:
                continue

            # --- CRITICAL LAG FIX ---
            # Move all tensors to CPU memory at once. 
            # Doing box.xyxy[0].tolist() inside a loop forces a GPU-to-CPU 
            # synchronization overhead for every single detected object, causing severe lag.
            boxes = result.boxes.cpu()
            
            xyxy_list = boxes.xyxy.numpy()
            conf_list = boxes.conf.numpy()
            cls_list = boxes.cls.numpy()

            # Safely iterate through fast local NumPy memory arrays
            for i in range(len(boxes)):
                detections.append({
                    "bbox": 
                        xyxy_list[i].tolist(),
                    "confidence": 
                        float(conf_list[i]),
                    "class_id": 
                        int(cls_list[i])
                })

        return detections
