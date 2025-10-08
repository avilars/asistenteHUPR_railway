#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Detectar y mostrar el último modelo entrenado
MODEL_PATH=$(ls -t models | head -1)
echo "✅ Modelo más reciente: $MODEL_PATH"

# Iniciar el servidor Rasa sin uvloop (soluciona error Event loop is closed)
python -m rasa run \
  --enable-api \
  --cors "*" \
  --host 0.0.0.0 \
  --port ${PORT:-8080} \
  -m models/$MODEL_PATH \
  --credentials credentials.yml \
  --endpoints endpoints.yml \
  --debug
