#!/usr/bin/env bash
# One-time server setup for Baithak backend.
# Run on your VPS as a user with docker access.
set -euo pipefail

REPO_URL="${1:-git@github.com:muhammadtalha198/baithak-backened.git}"
BRANCH="${2:-main}"
APP_DIR="${3:-/opt/baithak/backend}"

sudo mkdir -p "$(dirname "$APP_DIR")"
if [[ ! -d "$APP_DIR/.git" ]]; then
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  echo "Repo already exists at $APP_DIR"
fi

cd "$APP_DIR"
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env — edit it with production secrets before deploying."
fi

chmod +x scripts/deploy.sh
echo "Backend ready at $APP_DIR"
echo "Next: edit .env, then run ./scripts/deploy.sh"
