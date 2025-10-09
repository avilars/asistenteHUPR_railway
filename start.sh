#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Detectar y mostrar el último modelo entrenado
MODEL_PATH=$(ls -t models | head -1)
echo "✅ Modelo más reciente: $MODEL_PATH"

# Ejecutar el servidor Rasa
python -m rasa run \
  -m models/$MODEL_PATH \
  --enable-api \
  --cors "*" \
  --host 0.0.0.0 \
  --port ${PORT:-8080} \
  --credentials credentials.yml \
  --endpoints endpoints.yml \
  --debug
