import asyncio
import json
import logging
import math
import random
import time
import base64
import os
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Set, Optional
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("api-gateway")

app = FastAPI(
    title="PRECIS API Gateway",
    description="Backend coordinator for the Predictive Crowd Resonance & Intelligence System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try import CV libs optionally
try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    logger.warning("OpenCV not available - falling back to mock video processing")

# Connected WebSocket clients tracking
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        tasks = []
        for connection in list(self.active_connections):
            tasks.append(self.send_personal_message(message, connection))
        await asyncio.gather(*tasks, return_exceptions=True)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception:
            pass

manager = ConnectionManager()

# Global State
state = {
    "cci": 12.5,
    "ops": 5.0,
    "psi": 0.08,
    "decibel": 54.2,
    "person_count": 84,
    "stress_pitch_drift": 0.02,
    "screaming": False,
    "alarm_level": "GREEN",
    "dispatches": [],
    "recent_alerts": []
}

# Video source state - controls whether simulation runs
video_state = {
    "mode": "simulation",  # simulation | video_file | live
    "active": False,
    "filename": None,
    "progress": 0.0,
    "fps": 0,
    "total_frames": 0,
    "current_frame": 0,
}
video_task: Optional[asyncio.Task] = None
stop_video_flag = False
# When True, internal sine-wave simulation ticks even with no mocks/video.
# In production (python scripts/dev.py --gateway --ui) you want this False
# so the dashboard stays static until real video starts.
simulation_enabled = os.getenv("PRECIS_SIMULATION", "0") == "1"

# ---------- Helpers ----------
def compute_metrics(person_count: int, flow_divergence: float, decibel: float, stress_pitch: float, screaming: bool):
    psi = min(1.0, max(0.0, flow_divergence / 10.0))
    vision_factor = psi * 100
    vocal_factor = stress_pitch * 100
    decibel_factor = min(100.0, max(0.0, (decibel - 40) * 1.5))
    if screaming:
        decibel_factor = max(decibel_factor, 85.0)
    computed_cci = (vision_factor * 0.5) + (vocal_factor * 0.3) + (decibel_factor * 0.2)
    cci = round(min(100.0, max(0.0, computed_cci)), 1)
    ops_base = 100 / (1 + math.exp(-10 * (psi - 0.5)))
    ops = round(min(100.0, max(0.0, ops_base + (vocal_factor * 0.1))), 1)
    if cci >= 80:
        alarm = "RED"
    elif cci >= 55:
        alarm = "ORANGE"
    elif cci >= 30:
        alarm = "YELLOW"
    else:
        alarm = "GREEN"
    return cci, ops, psi, alarm

async def update_and_broadcast(trigger_reason: str):
    cci, ops, psi, alarm = compute_metrics(
        state["person_count"], state["psi"]*10 if state["psi"]<1 else state["psi"],
        state["decibel"], state["stress_pitch_drift"], state["screaming"]
    )
    # psi already in state; recompute via flow
    # Use direct formula with current psi
    vision_factor = state["psi"] * 100
    vocal_factor = state["stress_pitch_drift"] * 100
    decibel_factor = min(100.0, max(0.0, (state["decibel"] - 40) * 1.5))
    if state["screaming"]:
        decibel_factor = max(decibel_factor, 85.0)
    computed_cci = (vision_factor * 0.5) + (vocal_factor * 0.3) + (decibel_factor * 0.2)
    state["cci"] = round(min(100.0, max(0.0, computed_cci)), 1)
    ops_base = 100 / (1 + math.exp(-10 * (state["psi"] - 0.5)))
    state["ops"] = round(min(100.0, max(0.0, ops_base + (vocal_factor * 0.1))), 1)
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
        "data": state,
        "video_state": video_state
    }
    await manager.broadcast(payload)

async def broadcast_frame(b64_jpg: str, meta: dict):
    await manager.broadcast({
        "event": "video_frame",
        "timestamp": datetime.now().isoformat(),
        "frame": b64_jpg,
        "meta": meta,
        "data": state,
        "video_state": video_state
    })

def estimate_from_frame(frame, prev_gray=None):
    """Estimate person_count and flow_divergence from frame using OpenCV fallback."""
    if not HAS_CV2 or frame is None:
        return random.randint(30, 110), random.uniform(0.5, 2.5), random.uniform(52, 70)
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (320, 240))
        # Person count proxy: contour count on background-like threshold
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # filter by area
        cnt = len([c for c in contours if 200 < cv2.contourArea(c) < 5000])
        person_count = max(5, min(200, cnt * 3 + random.randint(-4,4)))
        # flow divergence via optical flow if prev available
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            mean_mag = float(np.mean(mag))
            std_mag = float(np.std(mag))
            divergence = round(min(10, mean_mag*5 + std_mag*2), 2)
        else:
            divergence = round(random.uniform(0.5, 1.5), 2)
        decibel = round(55 + person_count*0.15 + random.uniform(-2,2),1)
        return person_count, divergence, decibel
    except Exception as e:
        logger.warning(f"frame estimate fallback: {e}")
        return random.randint(30, 110), random.uniform(0.5, 2.5), random.uniform(52,70)

# ---------- Ingest endpoints ----------
class YOLOPayload(BaseModel):
    camera_id: str
    person_count: int
    mean_velocity_magnitude: float
    flow_divergence: float

@app.post("/api/ingest/yolo")
async def ingest_yolo(data: YOLOPayload):
    state["person_count"] = data.person_count
    state["psi"] = min(1.0, max(0.0, data.flow_divergence / 10.0))
    await update_and_broadcast("yolo_update")
    return {"status": "success"}

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

# ---------- Video: Upload ----------
@app.post("/api/video/upload")
async def upload_video(file: UploadFile = File(...)):
    global video_task, stop_video_flag
    # cancel previous
    if video_task and not video_task.done():
        stop_video_flag = True
        video_task.cancel()
        try:
            await video_task
        except asyncio.CancelledError:
            pass
    suffix = Path(file.filename).suffix or ".mp4"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    content = await file.read()
    tmp.write(content)
    tmp.close()
    logger.info(f"Uploaded video: {file.filename} ({len(content)} bytes) -> {tmp.name}")
    video_state.update({"mode": "video_file", "active": True, "filename": file.filename, "progress": 0.0, "current_frame": 0})
    stop_video_flag = False
    video_task = asyncio.create_task(process_video_file(tmp.name, file.filename))
    return {"status": "processing", "filename": file.filename, "tmp_path": tmp.name}

async def process_video_file(path: str, filename: str):
    global stop_video_flag
    try:
        if not HAS_CV2:
            # mock processing: 30 ticks
            for i in range(30):
                if stop_video_flag:
                    break
                state["person_count"] = random.randint(40, 130)
                state["psi"] = round(random.uniform(0.1, 0.7), 2)
                state["decibel"] = round(random.uniform(55, 75), 1)
                state["stress_pitch_drift"] = round(random.uniform(0.05, 0.4), 2)
                state["screaming"] = random.random() > 0.85
                video_state["progress"] = round((i+1)/30*100,1)
                video_state["current_frame"] = i
                await update_and_broadcast("video_file_tick")
                await asyncio.sleep(0.4)
            video_state["active"] = False
            if not stop_video_flag:
                video_state["mode"] = "simulation"
            try: os.unlink(path)
            except: pass
            return
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            logger.error(f"Cannot open video {path}")
            video_state["active"] = False
            return
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        video_state["total_frames"] = total
        video_state["fps"] = round(fps,1)
        # target processing fps 5
        step = max(1, int(fps // 5)) if fps>5 else 1
        idx = 0
        prev_gray = None
        while True:
            if stop_video_flag:
                break
            ret, frame = cap.read()
            if not ret:
                break
            if idx % step != 0:
                idx += 1
                continue
            # estimate
            gray_small = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),(320,240))
            pc, div, dec = estimate_from_frame(frame, prev_gray)
            prev_gray = gray_small
            state["person_count"] = pc
            state["psi"] = min(1.0, max(0.0, div/10.0))
            state["decibel"] = dec
            state["stress_pitch_drift"] = round(min(1, div*0.15 + random.uniform(0,0.05)),2)
            state["screaming"] = dec > 72 and random.random()>0.6
            video_state["progress"] = round((cap.get(cv2.CAP_PROP_POS_FRAMES)/total*100) if total else 0,1)
            video_state["current_frame"] = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            # encode frame with overlays
            vis = cv2.resize(frame, (640,360))
            cv2.putText(vis, f"CNT:{pc} PSI:{state['psi']:.2f}", (12,28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(vis, f"CCI:{state['cci']:.0f} {state['alarm_level']}", (12,56), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            _, buf = cv2.imencode('.jpg', vis, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            b64 = base64.b64encode(buf.tobytes()).decode()
            await update_and_broadcast("video_file_tick")
            await broadcast_frame(b64, {"frame_idx": idx, "progress": video_state["progress"]})
            idx += 1
            await asyncio.sleep(0.2)  # ~5 fps broadcast
        cap.release()
        try: os.unlink(path)
        except: pass
        if not stop_video_flag:
            video_state["active"] = False
            video_state["mode"] = "simulation"
            video_state["progress"] = 100.0
            await broadcast_state("video_file_done")
            logger.info("Video file processing done")
    except asyncio.CancelledError:
        logger.info("Video processing cancelled")
        try: os.unlink(path)
        except: pass
    except Exception as e:
        logger.error(f"process_video_file error: {e}")
        video_state["active"] = False

@app.post("/api/video/stop")
async def stop_video():
    global stop_video_flag, video_task
    stop_video_flag = True
    if video_task and not video_task.done():
        video_task.cancel()
        try: await video_task
        except: pass
    video_state.update({"mode": "simulation", "active": False, "progress": 0.0})
    await broadcast_state("video_stopped")
    return {"status": "stopped"}

@app.get("/api/video/status")
async def video_status():
    return video_state

# ---------- Video: Live frame ingest ----------
class LiveFramePayload(BaseModel):
    frame: str  # base64 jpg (with or without data:image prefix)
    camera_id: Optional[str] = "live"

@app.post("/api/video/live/frame")
async def ingest_live_frame(payload: LiveFramePayload):
    # decode
    b64 = payload.frame
    if "," in b64:
        b64 = b64.split(",",1)[1]
    try:
        if HAS_CV2:
            data = base64.b64decode(b64)
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            pc, div, dec = estimate_from_frame(frame)
            state["person_count"] = pc
            state["psi"] = min(1.0, max(0.0, div/10.0))
            state["decibel"] = dec
            state["stress_pitch_drift"] = round(min(1, div*0.12 + random.uniform(0,0.04)),2)
            # screaming heuristic
            state["screaming"] = dec > 70 and div > 1.2
        else:
            state["person_count"] = random.randint(30, 120)
            state["psi"] = round(random.uniform(0.08, 0.6),2)
            state["decibel"] = round(random.uniform(54, 74),1)
            state["stress_pitch_drift"] = round(random.uniform(0.02, 0.35),2)
        video_state.update({"mode": "live", "active": True})
        await update_and_broadcast("live_frame")
        # echo frame back with overlay via broadcast
        await broadcast_frame(b64, {"camera_id": payload.camera_id})
        return {"status": "ok", "state": state}
    except Exception as e:
        logger.error(f"live frame error: {e}")
        return JSONResponse(status_code=400, content={"status":"error","detail":str(e)})

@app.post("/api/video/live/start")
async def live_start():
    video_state.update({"mode": "live", "active": True})
    await broadcast_state("live_start")
    return {"status": "live_started"}

@app.post("/api/video/live/stop")
async def live_stop():
    video_state.update({"mode": "live", "active": False})
    # go back to simulation after live
    video_state["mode"] = "simulation"
    await broadcast_state("live_stopped")
    return {"status": "live_stopped"}

# ---------- Dispatch & Reset ----------
class DispatchRequest(BaseModel):
    alert_level: str

@app.post("/api/dispatch")
async def trigger_dispatch(req: DispatchRequest):
    dispatch_id = f"DSP-{int(time.time())}-{random.randint(100, 999)}"
    if req.alert_level == "RED":
        state["cci"] = 92.4; state["ops"] = 88.1; state["psi"] = 0.89; state["alarm_level"] = "RED"
        ap, am, af = 12,6,3
    elif req.alert_level == "ORANGE":
        state["cci"] = 68.2; state["ops"] = 55.4; state["psi"] = 0.61; state["alarm_level"] = "ORANGE"
        ap, am, af = 6,3,1
    else:
        state["cci"] = 42.1; state["ops"] = 31.8; state["psi"] = 0.42; state["alarm_level"] = "YELLOW"
        ap, am, af = 3,1,0
    new_dispatch = {
        "dispatch_id": dispatch_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alert_level": state["alarm_level"],
        "allocated_police_units": ap,
        "allocated_medical_units": am,
        "allocated_fire_units": af,
        "triage_zone": {"lat": 22.5726 + (random.random() - 0.5) * 0.01, "lng": 88.3639 + (random.random() - 0.5) * 0.01},
        "notified_hospitals": ["Ruby General Hospital", "Fortis Healthcare"] if req.alert_level == "RED" else ["Ruby General Hospital"],
        "status": "DISPATCHED"
    }
    state["dispatches"].insert(0, new_dispatch)
    alert_msg = f"Anticipatory Emergency Dispatch triggered. Level: {state['alarm_level']}. Police: {ap}, Med: {am}."
    state["recent_alerts"].insert(0, {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": alert_msg, "level": state["alarm_level"]})
    state["dispatches"] = state["dispatches"][:10]
    state["recent_alerts"] = state["recent_alerts"][:15]
    await broadcast_state("dispatch_triggered")
    return {"status": "dispatched", "dispatch_data": new_dispatch}

@app.post("/api/reset")
async def reset_state():
    state.update({"cci":12.5,"ops":5.0,"psi":0.08,"decibel":54.2,"person_count":84,"stress_pitch_drift":0.02,"screaming":False,"alarm_level":"GREEN","dispatches":[],"recent_alerts":[{"timestamp": datetime.now().strftime("%H:%M:%S"), "message": "System status normalized. Monitoring active.", "level": "GREEN"}]})
    video_state.update({"mode":"simulation","active":False,"progress":0.0})
    await broadcast_state("system_reset")
    return {"status": "reset"}

class SimulationToggle(BaseModel):
    enabled: bool

@app.post("/api/simulation")
async def set_simulation(payload: SimulationToggle):
    global simulation_enabled
    simulation_enabled = bool(payload.enabled)
    logger.info(f"Simulation {'enabled' if simulation_enabled else 'disabled'} via API")
    await broadcast_state("simulation_toggled")
    return {"simulation_enabled": simulation_enabled}

@app.get("/api/simulation")
async def get_simulation():
    return {"simulation_enabled": simulation_enabled, "mode": video_state["mode"], "active": video_state["active"]}

@app.get("/api/health")
async def health():
    return {"status":"ok", "mode": video_state["mode"], "has_cv2": HAS_CV2, "simulation_enabled": simulation_enabled}

@app.get("/health")
async def health2():
    return {"status":"healthy"}

# WebSocket
@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await websocket.send_json({"event": "initial_state","timestamp": datetime.now().isoformat(),"data": state, "video_state": video_state})
    try:
        while True:
            msg = await websocket.receive_text()
            try:
                payload = json.loads(msg)
                if payload.get("event") == "frame" and payload.get("frame"):
                    # live frame via WS (lower latency)
                    b64 = payload["frame"]
                    if "," in b64: b64 = b64.split(",",1)[1]
                    if HAS_CV2:
                        try:
                            data = base64.b64decode(b64)
                            nparr = np.frombuffer(data, np.uint8)
                            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                            pc, div, dec = estimate_from_frame(frame)
                            state["person_count"]=pc; state["psi"]=min(1.0, max(0.0, div/10.0)); state["decibel"]=dec
                            state["stress_pitch_drift"]=round(min(1, div*0.12+random.uniform(0,0.04)),2)
                            state["screaming"]= dec>70 and div>1.2
                            video_state.update({"mode":"live","active":True})
                            await update_and_broadcast("live_frame_ws")
                        except Exception as e:
                            logger.warning(f"WS frame decode fail {e}")
                    else:
                        state["person_count"]=random.randint(30,120)
                        await update_and_broadcast("live_frame_ws")
            except json.JSONDecodeError:
                logger.info(f"WS text: {msg}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Simulation loop - pauses when video active
async def crowd_simulation_loop():
    logger.info("Initializing Crowd Dynamics Background Simulation...")
    state["recent_alerts"].append({"timestamp": datetime.now().strftime("%H:%M:%S"),"message": "System status normalized. Monitoring active.","level": "GREEN"})
    cycle = 0.0
    while True:
        try:
            cycle += 0.05
            # ONLY simulate when explicitly enabled AND in simulation mode
            if simulation_enabled and video_state["mode"] == "simulation" and not video_state["active"]:
                if state["alarm_level"] in ["GREEN", "YELLOW"]:
                    state["person_count"] = int(100 + 15 * math.sin(cycle) + random.randint(-5, 5))
                    state["psi"] = round(0.15 + 0.08 * math.sin(cycle * 0.8) + random.uniform(-0.02, 0.02), 2)
                    state["decibel"] = round(56.0 + 4.0 * math.cos(cycle * 1.2) + random.uniform(-1.0, 1.0), 1)
                    state["stress_pitch_drift"] = round(0.04 + 0.03 * math.sin(cycle * 0.5) + random.uniform(-0.01, 0.01), 2)
                    state["screaming"] = False
                    if int(cycle * 10) % 400 == 0:
                        state["psi"] = 0.45; state["stress_pitch_drift"] = 0.38; state["decibel"] = 72.4; state["screaming"] = True
                        state["recent_alerts"].insert(0, {"timestamp": datetime.now().strftime("%H:%M:%S"),"message": "Acoustic anomaly detected. Analyzing spatial frequency...","level": "YELLOW"})
                else:
                    state["cci"] = max(12.5, state["cci"] - 1.5)
                    state["ops"] = max(5.0, state["ops"] - 2.0)
                    state["psi"] = max(0.08, state["psi"] - 0.02)
                    state["decibel"] = max(54.2, state["decibel"] - 0.8)
                    state["stress_pitch_drift"] = max(0.02, state["stress_pitch_drift"] - 0.01)
                    if state["cci"] < 30:
                        state["alarm_level"] = "GREEN"; state["screaming"] = False
                await update_and_broadcast("sim_tick")
            else:
                # when video/live active, just keep broadcasting current state occasionally
                await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
        await asyncio.sleep(1.5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(crowd_simulation_loop())
    logger.info("FastAPI Gateway started successfully.")
