#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Mostrar contenido de la carpeta models para verificar que el modelo está ahí
ls -l models

# Ejecutar Rasa con el modelo correcto
rasa run \
  -m models/20251008-214320-burgundy-band.tar.gz \
  --enable-api \
  --cors "*" \
  --credentials credentials.yml \
  --endpoints endpoints.yml \
  --host 0.0.0.0 \
  --port ${PORT:-5005}
