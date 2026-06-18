import cv2
import asyncio
import logging
import time  # Added for tracking metrics

from backend.api.routes.websocket_routes import manager
from ai_engine.multispectral.thermal_detector import ThermalDetector
from system_integration.predictive_pipeline import PredictivePipeline
from backend.services.incident_service import IncidentService
from backend.services.alert_service import AlertService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraStream:
    def __init__(self, source=0):
        self.source = source
        self.detector = ThermalDetector()
        self.pipeline = PredictivePipeline()

        # Initialize services
        self.incident_service = IncidentService()
        self.alert_service = AlertService()

    def start(self):
        # Force DirectShow backend on Windows
        cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)

        if not cap.isOpened():
            logger.error("Failed to open camera")
            return

        # Prevent OpenCV from buffering old frames to remove video processing lag
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Reduce downscaling resolution to optimize YOLO detection throughput
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        logger.info("Camera started... Press Q to quit.")

        # Performance Tuning: Throttling & Counter Initialization
        frame_count = 0
        last_detections = []
        last_broadcast = time.time()
        
        # Database Ingestion Throttling (10-second suppression window)
        last_incident_time = 0.0
        last_alert_time = 0.0

        # Initialize baseline clock time for FPS calculation loop
        prev_time = time.time()

        while True:
            success, frame = cap.read()
            if not success:
                logger.error("Failed to read frame")
                break

            # Live frame-by-frame FPS delta computation using safe denominator capping
            current_time = time.time()
            fps = 1 / max(current_time - prev_time, 0.001)
            prev_time = current_time

            frame_count += 1

            # Throttled dimension verification
            if frame_count % 100 == 0:
                logger.info(f"Frame shape: {frame.shape}")
                logger.info("Frame received")

            # Frame skipping layout to drop AI inference usage by ~66%
            try:
                if frame_count % 3 == 0:
                    last_detections = self.detector.detect(frame)
                    if frame_count % 100 == 0:
                        logger.info("YOLO executed")
                
                detections = last_detections
            except Exception as e:
                logger.exception("YOLO detection failed")
                continue

            density = len(detections)
            if frame_count % 100 == 0:
                logger.info(f"Person count: {density}")

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
            print("RISK SCORE:", risk_level)
            logger.info(f"Risk score: {risk_level}")

            # Context-aware pipeline allocation with 10-second database suppression
            if risk_level in ["MEDIUM", "HIGH", "CRITICAL"]:
                current_ts = time.time()
                
                # Suppress incident DB insertions unless 10 seconds have elapsed
                if current_ts - last_incident_time > 10.0:
                    incident = self.incident_service.create_incident(
                        camera_id="live_camera",
                        density=density,
                        risk_level=risk_level
                    )
                    logger.info(f"INCIDENT CREATED: {incident}")
                    last_incident_time = current_ts

                # Suppress alert notifications unless 10 seconds have elapsed
                if current_ts - last_alert_time > 10.0:
                    alert = self.alert_service.create_alert(
                        camera_id="live_camera",
                        risk_level=risk_level
                    )
                    logger.info(f"ALERT CREATED: {alert}")
                    last_alert_time = current_ts

            # Broadcast rate handling to enforce a max 1Hz socket update frequency
            if time.time() - last_broadcast > 1.0:
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
                
                last_broadcast = time.time()

            # Density overlay (placed at the top stack)
            cv2.putText(
                frame,
                f"Density: {density}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            # Risk overlay (placed in the middle stack)
            cv2.putText(
                frame,
                f"Risk: {risk_level}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            # Loop Update: Render FPS Counter overlay layout at target coordinate
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow("PRECIS Camera", frame)

            print("PREDICTION:", result)
            logger.info("\nPrediction Result:")
            logger.info(result)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    CameraStream().start()