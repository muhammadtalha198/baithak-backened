#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$APP_DIR"

if [[ ! -f .env ]]; then
  echo "Missing .env — copy .env.example to .env and fill production values."
  exit 1
fi

docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
echo "Backend is running on http://127.0.0.1:8000"
