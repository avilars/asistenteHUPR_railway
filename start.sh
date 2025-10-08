#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Mostrar el contenido del directorio de modelos
ls models

# Iniciar el servidor Rasa con el modelo ya entrenado
rasa run --enable-api --cors "*" --host 0.0.0.0 --port ${PORT:-5005} \
  -m models/20251008-214320-burgundy-band.tar.gz \
  --credentials credentials.yml --endpoints endpoints.yml
