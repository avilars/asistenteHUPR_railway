#!/usr/bin/env bash
set -euo pipefail

echo "[start.sh] Arrancando Rasa con PORT=${PORT:-5005}…"

exec rasa run \
  --enable-api \
  --cors "*" \
  --host "0.0.0.0" \
  --port "${PORT:-5005}" \
  --credentials "credentials.yml"
