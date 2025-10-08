#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Detectar y mostrar el último modelo entrenado
MODEL_PATH=$(ls -t models | head -1)
echo "✅ Modelo más reciente: $MODEL_PATH"

# Ejecutar el servidor Rasa
rasa run --enable-api --cors "*" \
  -i 0.0.0.0 -p ${PORT:-5005} \
  -m models/$MODEL_PATH \
  --credentials credentials.yml \
  --endpoints endpoints.yml
