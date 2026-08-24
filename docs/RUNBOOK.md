# PRECIS RUNBOOK — Mock vs Real, How to Run & Test

> Single source of truth for running the system in **Real** (frontend only + real video) vs **Mock/Demo** (simulated sensors) modes.

## 1. Architecture at a glance

| Path | What it is | Is it required for real video? |
|------|------------|-------------------------------|
| `services/api-gateway/main.py` | **Central FastAPI gateway** — owns `state {cci,ops,psi,decibel,person_count,screaming,alarm_level}` + `video_state {mode}` + WebSocket `ws://:8000/ws/stream` + all REST. **Only service the frontend talks to.** | ✅ Yes |
| `apps/dashboard/src/App.jsx` | React Vite dashboard (`http://localhost:3000`). Tabs: **Live Camera / Recorded Video / Telemetry**. Sends webcam frames at 2 FPS via WS `frame` or `POST /api/video/live/frame`, uploads files via `POST /api/video/upload`. | ✅ Yes |
| `ai_engine/yolo/yolo_detector.py` | **MOCK** — loops `CAM-01/02/03` with `random(45,120)` persons + `flow_divergence random(0.1,2.5)` → `POST /api/ingest/yolo` | ❌ Mock only |
| `cv-engine/optical-flow/cv_processor.py` | **MOCK** — loops `MIC-01/02` with `decibel/stress/scream` random → `POST /api/ingest/audio` | ❌ Mock only |
| `services/api-gateway/main.py:crowd_simulation_loop` | **Internal mock** — sine-wave `sim_tick` every 1.5s that drives CCI when `video_state.mode==simulation` | Auto-paused when real video active |
| `backend/*`, `streaming/*`, `cv_engine/camera/camera_stream.py` | Legacy / infra services (NATS, Redpanda, Postgres, auth, predict, incidents). Not used by current dashboard. | ❌ Optional |
| `scripts/dev.py` | Orchestrator — compiles `pyproject.toml`, creates `.venv` via `uv`, `npm install`, starts processes | — |

**Key insight from `services/api-gateway/main.py:90`:** `video_state.mode` controls source of truth:
- `simulation` + `active==false` → `crowd_simulation_loop` + mock ingest are active
- `video_file` / `live` + `active==true` → simulation is **paused** (`await asyncio.sleep(0.1)`), metrics come from `estimate_from_frame()` (OpenCV contours + `calcOpticalFlowFarneback`).

---

## 2. Prerequisites

- Python 3.10+, Node.js 18+, `uv` (`pip install uv`)
- Gateway venv needs `opencv-python` + `python-multipart` (added to `services/api-gateway/pyproject.toml:7`):
  ```toml
  dependencies = ["fastapi","uvicorn[standard]","pydantic","websockets","nats-py","aiokafka","python-multipart","opencv-python","numpy"]
  ```

---

## 3. How to run

### 3.1 First-time bootstrap
```powershell
python scripts/dev.py --setup
# compiles requirements.txt for gateway/yolo/cv, creates 3x .venv, runs npm install in apps/dashboard
```

### 3.2 Production / Real-video mode (recommended)
Frontend shows real webcam / uploaded file, **no fake traffic**:
```powershell
python scripts/dev.py --gateway --ui
# starts:
#  - FastAPI Gateway http://localhost:8000  (uvicorn main:app --port 8000 --reload)
#  - Vite Dashboard  http://localhost:3000
# NO yolo_detector / cv_processor
```

### 3.3 Demo / Stress-test mode (with mocks)
For investor demo where you want numbers moving without a camera:
```powershell
python scripts/dev.py
# = --all (default) — starts gateway + yolo + cv + ui
# You will see continuously:
#   POST /api/ingest/yolo 200 OK [CAM-01] 60 persons
#   POST /api/ingest/audio 200 OK [MIC-01] 75dB
#   WebSocket /ws/stream [accepted]
#
# To run only mocks without UI:
python scripts/dev.py --ai
```

### 3.4 Individual services (manual)
```powershell
# Gateway alone (from services/api-gateway/)
uv run uvicorn main:app --port 8000 --reload

# YOLO mock alone (from ai_engine/yolo/)
uv run python yolo_detector.py   # env GATEWAY_URL=http://localhost:8000/api/ingest/yolo

# CV mock alone (from cv-engine/optical-flow/)
uv run python cv_processor.py

# Dashboard alone (from apps/dashboard/)
npm run dev   # vite --port 3000 --host 0.0.0.0
```

---

## 4. What each endpoint does (gateway only)

| Method | Path | Used by | Description |
|--------|------|---------|-------------|
| `POST` | `/api/ingest/yolo` | yolo mock | `{camera_id, person_count, flow_divergence}` → updates `person_count/psi` → `update_and_broadcast()` |
| `POST` | `/api/ingest/audio` | cv mock | `{sensor_id, decibel_level, stress_pitch_drift, screaming_detected}` → updates audio state |
| `POST` | `/api/video/upload` | Recorded Video tab | `multipart file` → temp file → `process_video_file()` at 5 FPS (contour count + optical flow) → broadcasts `video_frame` (base64 jpg 640x360) + telemetry |
| `POST` | `/api/video/live/start` | Live Camera tab Start | sets `video_state.mode=live` |
| `POST` | `/api/video/live/frame` | Live Camera (HTTP fallback) | `{frame: base64}` decoded via `cv2.imdecode` → `estimate_from_frame()` |
| `POST` | `/api/video/live/stop` | Live Camera Stop | resets to `simulation` |
| `POST` | `/api/video/stop` | Recorded stop | cancels `video_task`, resets to `simulation` |
| `GET`  | `/api/video/status` | — | returns `video_state` |
| `POST` | `/api/dispatch` | Dispatch buttons | `{alert_level:YELLOW/ORANGE/RED}` → creates dispatch + alert |
| `POST` | `/api/reset` | Reset button | resets `state` + `video_state` |
| `GET`  | `/api/health`, `/health` | healthcheck | `has_cv2`, `mode` |
| `WS`   | `/ws/stream` | Dashboard | `initial_state` on connect, `video_frame` during real video, `frame` ingest from browser (preferred low-latency path) |

Calculation (`main.py:103 compute_metrics`): `psi=divergence/10`, `vision=psi*100*0.5+vocal*100*0.3+decibel*100*0.2`, `cci=vision`, `ops=100/(1+exp(-10*(psi-0.5)))+vocal*0.1`, alarm `RED>=80 ORANGE>=55 YELLOW>=30`.

---

## 5. Testing

### 5.1 Smoke test (no mocks)
```powershell
python scripts/dev.py --gateway --ui
# 1. Open http://localhost:3000 → header shows LIVE + GREEN + SIMULATION
# 2. Live Camera → Start Camera → allow permission → REC badge → CCI moves within 0.5s (2 FPS ingest)
# 3. Recorded Video → upload .mp4 → progress bar → annotated frames (CNT/PSI/CCI overlay) stream
# 4. Stop → returns to SIMULATION
```

### 5.2 Mock ingestion test (without browser)
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/ingest/yolo -ContentType "application/json" -Body '{"camera_id":"TEST","person_count":120,"mean_velocity_magnitude":1.2,"flow_divergence":6.5}'
# → {"status":"success"} , dashboard CCI jumps if connected
```

### 5.3 Automated tests (legacy)
```powershell
pytest tests/test_api.py tests/test_websocket.py tests/test_pipeline_smoke.py
pytest ai_engine/yolo/tests cv-engine/optical-flow/tests -k "not integration"
```

### 5.4 How to tell what is running
| Log line | Meaning |
|----------|---------|
| `Initializing Crowd Dynamics Background Simulation` | `crowd_simulation_loop` started (always) |
| `POST /api/ingest/yolo 200 OK [CAM-01] 60 persons` | **Mock** yolo active — will disappear if you run `--gateway --ui` |
| `Gateway offline ... Running in stand-alone mode` | Gateway crashed or not yet bound (was bug before `python-multipart` fix) |
| `Client connected. Total clients: N` | Browser WS connected |
| `CancelledError / KeyboardInterrupt` on shutdown | Normal `asyncio.sleep()` cancellation when you Ctrl+C |

---

## 6. Common tasks

- **Kill mock noise but keep demo sine-wave:** run `--gateway --ui` (you still get `sim_tick` drift; that's internal to gateway).
- **Kill everything except gateway:** `python scripts/dev.py --gateway`
- **Rebuild after pyproject change:** `python scripts/dev.py --setup` or `uv pip compile pyproject.toml -o requirements.txt` inside `services/api-gateway`.
- **Docker infra (optional):** `cd infra/docker && docker compose up -d` — Redpanda `:8080`, NATS `:4222`, Postgres `:5432`.

---

## 7. What is NOT used by dashboard (cleanup candidates)

`backend/api/routes/*` (`camera/*`, `predict/*`, `analytics/*`, `incidents/*`, `dashboard/summary`, `auth/login`), `streaming/*`, `cv_engine/camera/camera_stream.py` (uses `cv2.imshow` locally, not web). Either wire gateway to proxy them or delete to avoid confusion.

