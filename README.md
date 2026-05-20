# PRECIS / NEURAL-SHIELD CRIS v3 Monorepo

*Predictive Crowd Resonance & Intelligence System*  
*Government-Grade AI Infrastructure for Predictive Crowd Stability & Emergency Coordination*

This repository is designed as a clean, modular monorepo to isolate deep learning workloads, classical computer vision, microservices business logic, and user-facing dashboards.

---

## 🏛️ Repository Architecture

- **/apps/dashboard/**: Real-time React dashboard (Vite + npm) for visualizing Crowd Criticality Index (CCI), Outstroke Probability Score (OPS), and dispatch alerts.
- **/services/api-gateway/**: Central FastAPI server coordinating sensor ingestion, WebSocket streams, and dispatch actions. Isolated with `uv`.
- **/ai-engine/yolo/**: YOLOv8 person tracking and density mapping simulation. Isolated with `uv`.
- **/cv-engine/optical-flow/**: Classical OpenCV optical flow and audio analysis simulation. Isolated with `uv`.
- **/shared/schemas/**: Shared pydantic schemas defining event-driven interfaces.
- **/infra/docker/**: Docker compose files to provision database stores and event streams (Redpanda, NATS, PostgreSQL).
- **/scripts/dev.py**: Master execution script to bootstrap environments, install dependencies, and start services concurrently.

---

## 🚀 Get Started: Quick Setup

To run the entire system in isolated environments, follow these simple steps.

### 📋 Prerequisites
1. **Python 3.10+** (Active in system PATH)
2. **Node.js & npm** (For UI Dashboard)
3. **`uv`** (Fast Python package manager)
   - Install via pip if you don't have it: `pip install uv`

### 🔧 1. One-Click Bootstrap
Run the manager script with the `--setup` flag. This will automatically compile dependencies, create isolated Python virtual environments using `uv venv`, and install npm packages.
```bash
python scripts/dev.py --setup
```

### ⚡ 2. Start All Services
Launch the API Gateway, YOLO simulation, CV simulation, and the React frontend concurrently.
```bash
python scripts/dev.py
```
This starts:
- **FastAPI API Gateway** at [http://localhost:8000](http://localhost:8000)
- **Vite React Dashboard UI** at [http://localhost:3000](http://localhost:3000)
- **YOLO Video Detector Simulator** sending logs to the gateway.
- **OpenCV Optical Flow Simulator** sending logs to the gateway.

---

## 🐳 Running with Docker (Optional Infrastructure)

If you wish to spin up the message brokers (Redpanda/NATS) and database (PostgreSQL):

```bash
# Navigate to Docker infra directory
cd infra/docker

# Launch containers
docker compose up -d
```
- **Redpanda Console**: Access the event streams visualization dashboard at [http://localhost:8080](http://localhost:8080).
- **NATS Server**: Available on port `4222` for high-frequency pub-sub messages.
- **PostgreSQL Database**: Accessible on port `5432` (`postgres://admin:supersecretpassword@localhost:5432/precis`).
