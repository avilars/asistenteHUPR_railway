#!/usr/bin/env bash
echo "[start.sh] Iniciando Rasa con PORT=${PORT:-5005} ..."
exec python3 -m rasa run --enable-api --cors "*" --host 0.0.0.0 --port ${PORT:-5005} -m models --credentials credentials.yml
