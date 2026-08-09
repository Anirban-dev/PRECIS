import argparse
import asyncio
import logging
import os
import platform
import time

import cv2

from ai_engine.multispectral.thermal_detector import ThermalDetector
from backend.api.routes.websocket_routes import manager
from backend.services.alert_service import AlertService
from backend.services.incident_service import IncidentService
from system_integration.predictive_pipeline import PredictivePipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CameraStream:
    def __init__(
        self,
        source=0,
        camera_id="live_camera",
        display=False,
        process_every_n_frames=5,
        max_read_failures=10,
    ):
        self.source = source
        self.camera_id = camera_id
        self.display = display
        self.process_every_n_frames = max(1, int(process_every_n_frames))
        self.max_read_failures = max(1, int(max_read_failures))
        self.detector = ThermalDetector()
        self.pipeline = PredictivePipeline()
        self.incident_service = IncidentService()
        self.alert_service = AlertService()

    def _open_capture(self):
        backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY
        cap = cv2.VideoCapture(self.source, backend)
        if not cap.isOpened():
            logger.error("Failed to open camera source: %s", self.source)
            return None

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return cap

    async def _broadcast(self, payload):
        await manager.broadcast(payload)

    def _broadcast_safely(self, payload):
        try:
            asyncio.run(self._broadcast(payload))
        except RuntimeError:
            logger.warning("Skipping camera broadcast because an event loop is already running")
        except Exception:
            logger.exception("WebSocket broadcast failed")

    def _draw_overlay(self, frame, detections, density, risk_level, fps):
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
                2,
            )

        cv2.putText(frame, f"Density: {density}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Risk: {risk_level}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def start(self):
        cap = self._open_capture()
        if cap is None:
            return

        frame_count = 0
        last_detections = []
        last_broadcast = time.time()
        last_incident_time = 0.0
        last_alert_time = 0.0
        prev_time = time.time()
        read_failures = 0

        try:
            while True:
                success, frame = cap.read()
                if not success:
                    read_failures += 1
                    logger.warning(
                        "Failed to read frame %s/%s from %s",
                        read_failures,
                        self.max_read_failures,
                        self.source,
                    )
                    if read_failures >= self.max_read_failures:
                        logger.error("Stopping camera after repeated read failures")
                        break
                    time.sleep(0.2)
                    continue

                read_failures = 0
                frame_count += 1
                current_time = time.time()
                fps = 1 / max(current_time - prev_time, 0.001)
                prev_time = current_time

                if frame_count % self.process_every_n_frames == 0:
                    try:
                        last_detections = self.detector.detect(frame)
                    except Exception:
                        logger.exception("YOLO detection failed")
                        last_detections = []

                density = len(last_detections)
                result = self.pipeline.execute(
                    rgb_density=[density, density, density],
                    thermal_density=[density, density, density],
                    infrared_density=[density, density, density],
                    flow_vectors=[[1, 0], [0, 1]],
                    turbulence_score=density,
                )
                risk_level = result["risk"]["risk_level"]

                if risk_level in ["MEDIUM", "HIGH", "CRITICAL"]:
                    now = time.time()
                    if now - last_incident_time > 10.0:
                        incident = self.incident_service.create_incident(
                            camera_id=self.camera_id,
                            density=density,
                            risk_level=risk_level,
                        )
                        logger.info("Incident created: %s", incident)
                        last_incident_time = now

                    if now - last_alert_time > 10.0:
                        alert = self.alert_service.create_alert(
                            camera_id=self.camera_id,
                            risk_level=risk_level,
                        )
                        logger.info("Alert created: %s", alert)
                        last_alert_time = now

                if time.time() - last_broadcast > 1.0:
                    self._broadcast_safely(
                        {
                            "event": "camera_prediction",
                            "data": {
                                "camera_id": self.camera_id,
                                "density": density,
                                "risk_level": risk_level,
                                "prediction": result,
                            },
                        }
                    )
                    last_broadcast = time.time()

                if self.display:
                    self._draw_overlay(frame, last_detections, density, risk_level, fps)
                    cv2.imshow("PRECIS Camera", frame)
                    if cv2.waitKey(1) == ord("q"):
                        break
        finally:
            cap.release()
            if self.display:
                cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=os.getenv("PRECIS_CAMERA_SOURCE", "0"))
    parser.add_argument("--camera-id", default=os.getenv("PRECIS_CAMERA_ID", "live_camera"))
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--process-every-n-frames",
        type=int,
        default=int(os.getenv("PRECIS_CAMERA_PROCESS_EVERY_N_FRAMES", "5")),
    )
    args = parser.parse_args()
    source = int(args.source) if str(args.source).isdigit() else args.source

    CameraStream(
        source=source,
        camera_id=args.camera_id,
        display=not args.headless,
        process_every_n_frames=args.process_every_n_frames,
    ).start()
