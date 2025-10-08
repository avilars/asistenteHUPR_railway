#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."
rasa run --enable-api --cors "*" --host 0.0.0.0 --port ${PORT:-5005} -m models/$(ls -t models | head -1) --credentials credentials.yml --endpoints endpoints.yml
