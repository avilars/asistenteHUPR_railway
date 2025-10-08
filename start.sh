#!/usr/bin/env bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Mostrar contenido del directorio de modelos
ls models

# Ejecutar Rasa con el modelo entrenado
exec python3 -m rasa run --enable-api --cors "*" --host 0.0.0.0 --port ${PORT:-8080} \
  -m models/20251008-214320-burgundy-band.tar.gz \
  --credentials credentials.yml --endpoints endpoints.yml
