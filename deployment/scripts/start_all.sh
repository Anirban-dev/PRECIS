#!/bin/bash

# Start all containers in the background using root docker-compose
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$REPO_ROOT"
docker compose up -d