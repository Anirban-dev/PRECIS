from ultralytics import YOLO


class ThermalDetector:

    def __init__(

        self,

        model_path="ai_engine/models/thermal_yolov8.pt"
    ):

        self.model = YOLO(
            model_path
        )

    def detect(

        self,

        frame,

        confidence=0.35
    ):

        results = self.model.predict(

            source=frame,

            conf=confidence,

            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                detections.append({

                    "bbox":
                        box.xyxy[0].tolist(),

                    "confidence":
                        float(box.conf[0]),

                    "class_id":
                        int(box.cls[0])
                })

        return detections