#!/bin/bash
echo "[start.sh] Arrancando Rasa con PORT=${PORT}..."
rasa run --enable-api --cors "*" --host 0.0.0.0 --port ${PORT:-5005} -m models/$(ls -t models | head -n1) --credentials credentials.yml --endpoints endpoints.yml
