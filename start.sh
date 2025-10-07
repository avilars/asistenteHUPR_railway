#!/usr/bin/env bash
set -Eeuo pipefail
echo "[start.sh] Arrancando Rasa con PORT=${PORT:-5005}..."

# Activa el entorno virtual si existe
if [[ -d ".venv" ]]; then
  source .venv/bin/activate
fi

# Ejecuta el entrypoint correcto
exec python -m rasa.__main__ run --enable-api --cors "*" --host 0.0.0.0 --port "${PORT:-5005}"
