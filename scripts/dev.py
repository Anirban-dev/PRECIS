import subprocess
import sys
import os
import time
import argparse
from pathlib import Path

# Paths relative to the repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
GATEWAY_PATH = REPO_ROOT / "services" / "api-gateway"
YOLO_PATH = REPO_ROOT / "ai_engine" / "yolo"
CV_PATH = REPO_ROOT / "cv-engine" / "optical-flow"
DASHBOARD_PATH = REPO_ROOT / "apps" / "dashboard"

def print_banner(text):
    print("=" * 60)
    print(f" {text.center(58)} ")
    print("=" * 60)

def run_command_in_bg(args, cwd, name):
    print(f"[*] Starting {name}...")
    # Use shell=True for windows command execution compatibility
    p = subprocess.Popen(args, cwd=str(cwd), shell=True)
    return p

def main():
    parser = argparse.ArgumentParser(description="PRECIS / NEURAL-SHIELD Monorepo Manager")
    parser.add_argument("--setup", action="store_true", help="Bootstrap packages and environments using uv and npm")
    parser.add_argument("--gateway", action="store_true", help="Start FastAPI Gateway only")
    parser.add_argument("--ai", action="store_true", help="Start YOLO & CV engines only")
    parser.add_argument("--ui", action="store_true", help="Start React Dashboard only")
    parser.add_argument("--all", action="store_true", help="Start all services (default)")
    
    args = parser.parse_args()
    
    # If no flags are passed, default to all
    if not (args.setup or args.gateway or args.ai or args.ui):
        args.all = True

    if args.setup:
        print_banner("BOOTSTRAPPING ENVIRONMENTS")
        
        # Verify uv is installed
        try:
            subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("[✓] 'uv' is installed and active.")
        except Exception:
            print("[!] Warning: 'uv' was not found in PATH. Please run: pip install uv")
            sys.exit(1)

        # 1. Setup API Gateway
        print("\n[*] Initializing services/api-gateway virtual environment...")
        subprocess.run(["uv", "pip", "compile", "pyproject.toml", "-o", "requirements.txt"], cwd=str(GATEWAY_PATH), shell=True)
        subprocess.run(["uv", "venv"], cwd=str(GATEWAY_PATH), shell=True)
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], cwd=str(GATEWAY_PATH), shell=True)
        print("[✓] API Gateway environment setup complete.")

        # 2. Setup YOLO Engine
        print("\n[*] Initializing ai_engine/yolo virtual environment...")
        subprocess.run(["uv", "pip", "compile", "pyproject.toml", "-o", "requirements.txt"], cwd=str(YOLO_PATH), shell=True)
        subprocess.run(["uv", "venv"], cwd=str(YOLO_PATH), shell=True)
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], cwd=str(YOLO_PATH), shell=True)
        print("[✓] YOLO Engine environment setup complete.")

        # 3. Setup CV Engine
        print("\n[*] Initializing cv-engine/optical-flow virtual environment...")
        subprocess.run(["uv", "pip", "compile", "pyproject.toml", "-o", "requirements.txt"], cwd=str(CV_PATH), shell=True)
        subprocess.run(["uv", "venv"], cwd=str(CV_PATH), shell=True)
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], cwd=str(CV_PATH), shell=True)
        print("[✓] CV Engine environment setup complete.")

        # 4. Setup Frontend Dashboard
        print("\n[*] Bootstrapping apps/dashboard packages (npm install)...")
        subprocess.run(["npm", "install"], cwd=str(DASHBOARD_PATH), shell=True)
        print("[✓] React Dashboard packages setup complete.")
        
        print_banner("SETUP SUCCESSFUL. RUN `python dev.py` TO START SERVICES.")
        return

    processes = []
    
    try:
        if args.gateway or args.all:
            # Boot FastAPI server
            gateway_cmd = ["uv", "run", "uvicorn", "main:app", "--port", "8000", "--reload"]
            p_gate = run_command_in_bg(gateway_cmd, GATEWAY_PATH, "FastAPI Gateway (Port 8000)")
            processes.append(p_gate)
            time.sleep(2)  # Give gateway time to bind ports

        if args.ai or args.all:
            # Boot YOLO Detector simulation
            yolo_cmd = ["uv", "run", "python", "yolo_detector.py"]
            p_yolo = run_command_in_bg(yolo_cmd, YOLO_PATH, "YOLO Detector (Cam simulation)")
            processes.append(p_yolo)

            # Boot CV Processor simulation
            cv_cmd = ["uv", "run", "python", "cv_processor.py"]
            p_cv = run_command_in_bg(cv_cmd, CV_PATH, "CV Optical Flow Processor (Audio simulation)")
            processes.append(p_cv)

        if args.ui or args.all:
            # Boot React Dashboard UI
            dashboard_cmd = ["npm", "run", "dev"]
            p_ui = run_command_in_bg(dashboard_cmd, DASHBOARD_PATH, "React Dashboard UI (Port 3000)")
            processes.append(p_ui)

        print_banner("ALL SERVICES RUNNING. PRESS CTRL+C TO STOP.")
        
        # Keep main thread alive and monitor children status
        while True:
            for p in processes:
                if p.poll() is not None:
                    print(f"[!] Warning: One of the child processes has exited with code {p.returncode}")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[*] Terminating all services...")
        for p in processes:
            p.terminate()
            p.wait()
        print("[✓] All services stopped.")

if __name__ == "__main__":
    main()
