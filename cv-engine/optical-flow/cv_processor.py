import time
import random
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("cv-processor")

GATEWAY_URL = "http://localhost:8000/api/ingest/audio"

def run_cv_processor():
    logger.info("Initializing OpenCV Optical Flow & Wave Analysis Engine...")
    logger.info("Calibrating grid matrices for motion fields...")
    
    sensor_ids = ["MIC-01", "MIC-02"]
    
    while True:
        try:
            # We simulate psycho-acoustic and sound telemetry
            for sensor in sensor_ids:
                decibels = random.uniform(50.0, 78.0)
                # Vocal stress drift (0 to 1 scale)
                stress_drift = random.uniform(0.01, 0.20)
                screaming = False
                
                # Random emergency event spike simulation (5% chance)
                if random.random() < 0.05:
                    decibels = random.uniform(85.0, 102.0)
                    stress_drift = random.uniform(0.70, 0.95)
                    screaming = True
                    logger.warning(f"[{sensor}] High amplitude stress wave detected!")

                payload = {
                    "sensor_id": sensor,
                    "decibel_level": round(decibels, 1),
                    "stress_pitch_drift": round(stress_drift, 2),
                    "screaming_detected": screaming
                }
                
                try:
                    res = requests.post(GATEWAY_URL, json=payload, timeout=2)
                    if res.status_code == 200:
                        logger.info(f"[{sensor}] Ingest success: {decibels} dB, stress: {stress_drift}, scream: {screaming}")
                except requests.exceptions.RequestException:
                    logger.warning(f"Gateway offline at {GATEWAY_URL}. Running in stand-alone mode.")
                    
            time.sleep(3.0)
            
        except Exception as e:
            logger.error(f"CV Processor error: {e}")
            time.sleep(5.0)

if __name__ == "__main__":
    run_cv_processor()
