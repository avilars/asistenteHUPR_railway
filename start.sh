#!/bin/bash
echo "[start.sh] Arrancando Rasa con PORT=${PORT:-5005}..."
rasa run --enable-api --cors "*" --host "0.0.0.0" --port ${PORT:-5005} -m models --credentials credentials.yml
