from ultralytics import YOLO


class WeaponDetector:

    def __init__(self):

        self.model = YOLO(
            "yolov8n.pt"
        )

    def detect(

        self,

        frame
    ):

        results = self.model.predict(

            source=frame,

            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = map(

                    int,

                    box.xyxy[0]
                )

                confidence = float(
                    box.conf[0]
                )

                detections.append({

                    "bbox":
                        [x1, y1, x2, y2],

                    "confidence":
                        confidence
                })

        return detections