import asyncio
import time
import random
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("yolo-detector")

GATEWAY_URL = "http://localhost:8000/api/ingest/yolo"

async def run_detector():
    logger.info("Initializing YOLOv8 Detector skeleton...")
    logger.info("Connecting to video streams (mock)...")
    
    camera_ids = ["CAM-01", "CAM-02", "CAM-03"]
    
    while True:
        try:
            # Simulate processing frame by frame for each camera
            for cam in camera_ids:
                # Generate mock detections
                person_count = random.randint(45, 120)
                mean_velocity = random.uniform(0.2, 1.8)
                
                # Flow divergence (PSI indicator) - standard crowd has low divergence.
                # High values imply turbulent flow / panic splits.
                flow_divergence = random.uniform(0.1, 2.5)
                
                payload = {
                    "camera_id": cam,
                    "person_count": person_count,
                    "mean_velocity_magnitude": round(mean_velocity, 2),
                    "flow_divergence": round(flow_divergence, 2)
                }
                
                # Try publishing to API Gateway
                try:
                    res = requests.post(GATEWAY_URL, json=payload, timeout=2)
                    if res.status_code == 200:
                        logger.info(f"[{cam}] Ingest success: {person_count} persons, divergence: {payload['flow_divergence']}")
                except requests.exceptions.RequestException:
                    logger.warning(f"Gateway offline at {GATEWAY_URL}. Running in stand-alone mode.")
                
            await asyncio.sleep(2.0)
            
        except Exception as e:
            logger.error(f"Detector loop error: {e}")
            await asyncio.sleep(5.0)

if __name__ == "__main__":
    asyncio.run(run_detector())
