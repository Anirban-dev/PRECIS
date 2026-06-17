import cv2
import asyncio
import logging

from backend.api.routes.websocket_routes import manager
from ai_engine.multispectral.thermal_detector import ThermalDetector
from system_integration.predictive_pipeline import PredictivePipeline

logger = logging.getLogger(__name__)

class CameraStream:
    def __init__(self, source=0):
        self.source = source
        self.detector = ThermalDetector()
        self.pipeline = PredictivePipeline()

    def start(self):
        cap = cv2.VideoCapture(self.source)

        if not cap.isOpened():
            logger.error("Failed to open camera")
            return

        logger.info("Camera started... Press Q to quit.")

        while True:
            success, frame = cap.read()
            if not success:
                logger.error("Failed to read frame")
                break

            # YOLO detection with error handling
            try:
                detections = self.detector.detect(frame)
            except Exception as e:
                logger.exception("YOLO detection failed")
                continue

            density = len(detections)

            # Draw detection boxes
            for detection in detections:
                x1, y1, x2, y2 = map(int, detection["bbox"])
                confidence = round(detection["confidence"], 2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{confidence}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            result = self.pipeline.execute(
                rgb_density=[density, density, density],
                thermal_density=[density, density, density],
                infrared_density=[density, density, density],
                flow_vectors=[[1, 0], [0, 1]],
                turbulence_score=density
            )

            risk_level = result["risk"]["risk_level"]

            # Broadcast prediction to websocket clients
            try:
                asyncio.run(
                    manager.broadcast(
                        {
                            "event": "camera_prediction",
                            "density": density,
                            "risk": risk_level,
                            "prediction": result
                        }
                    )
                )
            except Exception as e:
                logger.error(f"WebSocket Broadcast Error: {str(e)}")

            # Density overlay
            cv2.putText(
                frame,
                f"Density: {density}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            # Risk overlay
            cv2.putText(
                frame,
                f"Risk: {risk_level}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            cv2.imshow("PRECIS Camera", frame)

            logger.info("\nPrediction Result:")
            logger.info(result)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    CameraStream().start()
