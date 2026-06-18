from ultralytics import YOLO


class ThermalDetector:

    def __init__(
        self,
        model_path="ai_engine/models/thermal_yolov8.pt"
    ):
        self.model = YOLO(
            model_path
        )
        
        # Warm up the model at startup using your targeted resolution
        self.model.predict(source=None, imgsz=640, verbose=False)

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