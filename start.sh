#!/usr/bin/env bash
set -euo pipefail

echo "[start.sh] Arrancando Rasa con PORT=${PORT:-5005}…"

# Selecciona el último modelo entrenado
MODEL_PATH=$(ls -t models/*.tar.gz | head -n 1)

exec rasa run \
  -m "${MODEL_PATH}" \
  --enable-api \
  --cors "*" \
  --host 0.0.0.0 \
  --port "${PORT:-5005}" \
  --credentials credentials.yml