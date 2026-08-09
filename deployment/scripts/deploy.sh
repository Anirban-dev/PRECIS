#!/bin/bash

# PRECIS deployment script for Docker/Kubernetes environments
# Exit immediately if a command exits with a non-zero status
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$REPO_ROOT"

echo "============================================================"
echo "  PRECIS Deployment Tool"
echo "============================================================"

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "[!] Error: 'docker' command not found."
    exit 1
fi

echo "[*] Building all service images via Docker Compose..."
docker compose build

echo "[*] Starting all PRECIS containers..."
docker compose up -d

echo "[✓] Deployment complete! Dashboard running at http://localhost:3000"
echo "[*] Use 'docker compose ps' to monitor status or check logs with 'docker compose logs -f'"