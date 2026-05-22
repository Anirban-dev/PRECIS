import asyncio
import json
import logging
import math
import random
import time
from datetime import datetime
from typing import List, Dict, Any, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("api-gateway")

app = FastAPI(
    title="PRECIS API Gateway",
    description="Backend coordinator for the Predictive Crowd Resonance & Intelligence System"
)

# Enable CORS for frontend dashboard development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connected WebSocket clients tracking
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        # Create a list of tasks for concurrent sending
        tasks = []
        for connection in self.active_connections:
            tasks.append(self.send_personal_message(message, connection))
        await asyncio.gather(*tasks, return_exceptions=True)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception:
            # Handle disconnected or broken sockets
            pass

manager = ConnectionManager()

# Global State for tracking the latest telemetry (Vision, Audio, Criticality, Dispatch)
state = {
    "cci": 12.5,                # Crowd Criticality Index (0-100)
    "ops": 5.0,                 # Outstroke Probability Score (0-100)
    "psi": 0.08,                # Phase State Index (0-1)
    "decibel": 54.2,            # Audio intensity (dB)
    "person_count": 84,         # Detected crowd size
    "stress_pitch_drift": 0.02, # Vocal stress level (0-1)
    "screaming": False,
    "alarm_level": "GREEN",     # GREEN, YELLOW, ORANGE, RED
    "dispatches": [],
    "recent_alerts": []
}

# Ingest endpoint for YOLO vision metrics
class YOLOPayload(BaseModel):
    camera_id: str
    person_count: int
    mean_velocity_magnitude: float
    flow_divergence: float

@app.post("/api/ingest/yolo")
async def ingest_yolo(data: YOLOPayload):
    # Recalculate states based on input
    state["person_count"] = data.person_count
    # Divergence influences Phase State Index
    state["psi"] = min(1.0, max(0.0, data.flow_divergence / 10.0))
    await update_and_broadcast("yolo_update")
    return {"status": "success"}

# Ingest endpoint for Audio sensors
class AudioPayload(BaseModel):
    sensor_id: str
    decibel_level: float
    stress_pitch_drift: float
    screaming_detected: bool

@app.post("/api/ingest/audio")
async def ingest_audio(data: AudioPayload):
    state["decibel"] = data.decibel_level
    state["stress_pitch_drift"] = data.stress_pitch_drift
    state["screaming"] = data.screaming_detected
    await update_and_broadcast("audio_update")
    return {"status": "success"}

# Manually trigger a mock emergency cascade (Investor Demo / Control Room action)
class DispatchRequest(BaseModel):
    alert_level: str  # YELLOW, ORANGE, RED

@app.post("/api/dispatch")
async def trigger_dispatch(req: DispatchRequest):
    dispatch_id = f"DSP-{int(time.time())}-{random.randint(100, 999)}"
    
    if req.alert_level == "RED":
        state["cci"] = 92.4
        state["ops"] = 88.1
        state["psi"] = 0.89
        state["alarm_level"] = "RED"
        allocated_police = 12
        allocated_medical = 6
        allocated_fire = 3
    elif req.alert_level == "ORANGE":
        state["cci"] = 68.2
        state["ops"] = 55.4
        state["psi"] = 0.61
        state["alarm_level"] = "ORANGE"
        allocated_police = 6
        allocated_medical = 3
        allocated_fire = 1
    else:
        state["cci"] = 42.1
        state["ops"] = 31.8
        state["psi"] = 0.42
        state["alarm_level"] = "YELLOW"
        allocated_police = 3
        allocated_medical = 1
        allocated_fire = 0

    new_dispatch = {
        "dispatch_id": dispatch_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alert_level": state["alarm_level"],
        "allocated_police_units": allocated_police,
        "allocated_medical_units": allocated_medical,
        "allocated_fire_units": allocated_fire,
        "triage_zone": {"lat": 22.5726 + (random.random() - 0.5) * 0.01, "lng": 88.3639 + (random.random() - 0.5) * 0.01},
        "notified_hospitals": ["Ruby General Hospital", "Fortis Healthcare"] if req.alert_level == "RED" else ["Ruby General Hospital"],
        "status": "DISPATCHED"
    }
    
    state["dispatches"].insert(0, new_dispatch)
    alert_msg = f"Anticipatory Emergency Dispatch triggered. Level: {state['alarm_level']}. Police: {allocated_police}, Med: {allocated_medical}."
    state["recent_alerts"].insert(0, {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": alert_msg, "level": state["alarm_level"]})
    
    # Prune lists
    state["dispatches"] = state["dispatches"][:10]
    state["recent_alerts"] = state["recent_alerts"][:15]
    
    await broadcast_state("dispatch_triggered")
    return {"status": "dispatched", "dispatch_data": new_dispatch}

# Reset demo state to normal
@app.post("/api/reset")
async def reset_state():
    state["cci"] = 12.5
    state["ops"] = 5.0
    state["psi"] = 0.08
    state["decibel"] = 54.2
    state["person_count"] = 84
    state["stress_pitch_drift"] = 0.02
    state["screaming"] = False
    state["alarm_level"] = "GREEN"
    state["dispatches"] = []
    state["recent_alerts"] = [{"timestamp": datetime.now().strftime("%H:%M:%S"), "message": "System status normalized. Monitoring active.", "level": "GREEN"}]
    await broadcast_state("system_reset")
    return {"status": "reset"}

# Calculate overall threat score based on telemetry inputs
async def update_and_broadcast(trigger_reason: str):
    # CCI is computed as a weighted fusion: 50% Vision density/turbulence, 30% Vocal stress, 20% Sound amplitude
    vision_factor = state["psi"] * 100
    vocal_factor = state["stress_pitch_drift"] * 100
    decibel_factor = min(100.0, max(0.0, (state["decibel"] - 40) * 1.5))
    
    if state["screaming"]:
        decibel_factor = max(decibel_factor, 85.0)

    computed_cci = (vision_factor * 0.5) + (vocal_factor * 0.3) + (decibel_factor * 0.2)
    state["cci"] = round(min(100.0, max(0.0, computed_cci)), 1)

    # Outstroke (Crowd Surge) probability propagates nonlinearly relative to crowd density (PSI)
    # We model it using a sigmoid-like projection
    ops_base = 100 / (1 + math.exp(-10 * (state["psi"] - 0.5)))
    state["ops"] = round(min(100.0, max(0.0, ops_base + (vocal_factor * 0.1))), 1)

    # Determine Alarm Level thresholds
    if state["cci"] >= 80:
        state["alarm_level"] = "RED"
    elif state["cci"] >= 55:
        state["alarm_level"] = "ORANGE"
    elif state["cci"] >= 30:
        state["alarm_level"] = "YELLOW"
    else:
        state["alarm_level"] = "GREEN"

    await broadcast_state(trigger_reason)

async def broadcast_state(event_type: str):
    payload = {
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "data": state
    }
    await manager.broadcast(payload)

# Real-time WebSocket feed for dashboard
@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send initial state immediately
    await websocket.send_json({
        "event": "initial_state",
        "timestamp": datetime.now().isoformat(),
        "data": state
    })
    
    try:
        while True:
            # Maintain active connection, listen for client commands (if any)
            data = await websocket.receive_text()
            logger.info(f"Received message from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background Task: Simulation of crowd dynamics when external cameras/sensors are offline
async def crowd_simulation_loop():
    logger.info("Initializing Crowd Dynamics Background Simulation...")
    state["recent_alerts"].append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "message": "System status normalized. Monitoring active.",
        "level": "GREEN"
    })
    
    cycle = 0.0
    while True:
        try:
            # We simulate normal fluctuations, with occasional surges to demonstrate predictive capabilities
            # To keep things dynamic, we follow a sine wave for core crowd fluctuations, plus random walks
            cycle += 0.05
            
            # If the user or another API call has forced the state to RED/ORANGE, we let it slowly decay back to normal
            # instead of overwriting it instantly, or we run standard simulation if currently in GREEN.
            if state["alarm_level"] in ["GREEN", "YELLOW"]:
                # Normal crowd drift
                # Base person count around 100 with small oscillation
                state["person_count"] = int(100 + 15 * math.sin(cycle) + random.randint(-5, 5))
                
                # Flow divergence (PSI) fluctuates softly between 0.05 and 0.25
                state["psi"] = round(0.15 + 0.08 * math.sin(cycle * 0.8) + random.uniform(-0.02, 0.02), 2)
                
                # Decibels drift between 50 and 65 dB
                state["decibel"] = round(56.0 + 4.0 * math.cos(cycle * 1.2) + random.uniform(-1.0, 1.0), 1)
                
                # Vocal stress remains low
                state["stress_pitch_drift"] = round(0.04 + 0.03 * math.sin(cycle * 0.5) + random.uniform(-0.01, 0.01), 2)
                state["screaming"] = False
                
                # Periodically trigger a minor warning event to show off the dynamics (every 40 cycles)
                if int(cycle * 10) % 400 == 0:
                    state["psi"] = 0.45
                    state["stress_pitch_drift"] = 0.38
                    state["decibel"] = 72.4
                    state["screaming"] = True
                    alert_msg = "Acoustic anomaly detected. Analyzing spatial frequency..."
                    state["recent_alerts"].insert(0, {
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "message": alert_msg,
                        "level": "YELLOW"
                    })
            else:
                # Emergency decay: slowly lower values back down to normal
                state["cci"] = max(12.5, state["cci"] - 1.5)
                state["ops"] = max(5.0, state["ops"] - 2.0)
                state["psi"] = max(0.08, state["psi"] - 0.02)
                state["decibel"] = max(54.2, state["decibel"] - 0.8)
                state["stress_pitch_drift"] = max(0.02, state["stress_pitch_drift"] - 0.01)
                
                if state["cci"] < 30:
                    state["alarm_level"] = "GREEN"
                    state["screaming"] = False

            await update_and_broadcast("sim_tick")
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
            
        await asyncio.sleep(1.5)  # Tick rate

@app.on_event("startup")
async def startup_event():
    # Run the crowd simulation in the background
    asyncio.create_task(crowd_simulation_loop())
    logger.info("FastAPI Gateway started successfully.")
