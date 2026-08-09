#!/bin/bash

# PRECIS / NEURAL-SHIELD Monorepo dev runner for Linux
# Exit immediately if a command exits with a non-zero status
set -e

# Paths relative to the script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

GATEWAY_PATH="$REPO_ROOT/services/api-gateway"
YOLO_PATH="$REPO_ROOT/ai_engine/yolo"
CV_PATH="$REPO_ROOT/cv-engine/optical-flow"
DASHBOARD_PATH="$REPO_ROOT/apps/dashboard"

print_banner() {
    echo "============================================================"
    echo "  $1"
    echo "============================================================"
}

setup_environments() {
    print_banner "BOOTSTRAPPING ENVIRONMENTS"

    # Verify uv is installed
    if ! command -v uv &> /dev/null; then
        echo "[!] Error: 'uv' package manager is not installed."
        echo "Please install it using: pip install uv"
        exit 1
    fi

    # 1. Setup API Gateway
    echo -e "\n[*] Initializing services/api-gateway virtual environment..."
    cd "$GATEWAY_PATH"
    uv pip compile pyproject.toml -o requirements.txt
    uv venv
    uv pip install -r requirements.txt

    # 2. Setup YOLO Engine
    echo -e "\n[*] Initializing ai_engine/yolo virtual environment..."
    cd "$YOLO_PATH"
    uv pip compile pyproject.toml -o requirements.txt
    uv venv
    uv pip install -r requirements.txt

    # 3. Setup CV Engine
    echo -e "\n[*] Initializing cv-engine/optical-flow virtual environment..."
    cd "$CV_PATH"
    uv pip compile pyproject.toml -o requirements.txt
    uv venv
    uv pip install -r requirements.txt

    # 4. Setup Frontend Dashboard
    echo -e "\n[*] Bootstrapping apps/dashboard packages (npm install)..."
    cd "$DASHBOARD_PATH"
    npm install

    print_banner "SETUP SUCCESSFUL. RUN './scripts/dev.sh' TO START SERVICES."
}

start_services() {
    # Trap SIGINT and SIGTERM to kill all background jobs
    trap 'kill 0' SIGINT SIGTERM EXIT

    print_banner "STARTING ALL PRECIS SERVICES"

    # 1. Boot FastAPI server
    echo "[*] Starting FastAPI Gateway..."
    cd "$GATEWAY_PATH"
    uv run uvicorn main:app --port 8000 --host 0.0.0.0 --reload &
    sleep 2  # Give gateway time to bind ports

    # 2. Boot YOLO Detector simulation
    echo "[*] Starting YOLO Detector simulation..."
    cd "$YOLO_PATH"
    uv run python yolo_detector.py &

    # 3. Boot CV Processor simulation
    echo "[*] Starting CV Optical Flow Processor simulation..."
    cd "$CV_PATH"
    uv run python cv_processor.py &

    # 4. Boot React Dashboard UI
    echo "[*] Starting React Dashboard UI..."
    cd "$DASHBOARD_PATH"
    npm run dev &

    print_banner "ALL SERVICES RUNNING. PRESS CTRL+C TO STOP."

    # Keep script alive and monitor background jobs
    wait
}

if [ "$1" == "--setup" ]; then
    setup_environments
else
    start_services
fi
